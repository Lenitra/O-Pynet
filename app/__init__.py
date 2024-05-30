import os
import importlib
from flask import Flask, Blueprint

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
            module_name = f'app.routes.{filename[:-3]}'
            module = importlib.import_module(module_name)
            
            # Si le module contient un Blueprint, on l'enregistre
            for attr in dir(module):
                obj = getattr(module, attr)
                if isinstance(obj, Blueprint):
                    app.register_blueprint(obj)

    return app
