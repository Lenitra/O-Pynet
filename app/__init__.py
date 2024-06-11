import os
import importlib
from flask import Flask, Blueprint
import json
from app.aaa import wirteCommonJS

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    

    # Configuration des templates et des fichiers statiques
    app.template_folder = 'templates'
    app.static_folder = 'static'

    # Chemin vers le dossier des routes
    routes_dir = os.path.join(os.path.dirname(__file__), 'routes')

    # Importer tous les fichiers .py dans le dossier des routes
    for filename in os.listdir(routes_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            
            # Regarde les modules à ne pas charger dans le fichier config.json
            with open("config.json") as f:
                config = json.load(f)
            try:
                if config["modules"][filename[:-3]] == False:
                    continue
            except:
                pass
            
            if filename == "spotify.py":
                if config["spotify"]["client_id"] == "" or config["spotify"]["client_secret"] == "":
                    config["modules"]["spotify"] = False
                    continue
                
            module_name = f'app.routes.{filename[:-3]}'
            module = importlib.import_module(module_name)
            
            # Si le module contient un Blueprint, on l'enregistre
            for attr in dir(module):
                obj = getattr(module, attr)
                if isinstance(obj, Blueprint):
                    app.register_blueprint(obj)
                    print(f"Module {filename[:-3]} chargé")

    # enregistre le fichier config.json
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
    
    # Créer le fichier commun.js
    wirteCommonJS()

    return app
