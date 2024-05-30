from flask import Blueprint, send_file, session, redirect, render_template, jsonify, send_file
import psutil
import json
import os

FILES = Blueprint('files', __name__)



@FILES.route('/download/<path:file_path>')
def download_file(file_path):
    if 'user' not in session:
        return redirect("/login")
    # Obtenir le chemin complet du fichier à télécharger
    full_path = os.path.join('./', file_path)

    # Vérifier si le fichier existe
    if os.path.isfile(full_path):
        # Envoyer le fichier au client pour téléchargement
        return send_file(full_path, as_attachment=True)
    else:
        return 'Le fichier spécifié n\'existe pas.', 404




@FILES.route('/files')
def get_discks():
    if 'user' not in session:
        return redirect("/login")
    
    # lister les disques
    files_data = []
    for part in psutil.disk_partitions():
        files_data.append({
            'name': part.device.split("\\")[0],
            'type': 'directory'
        })

    # Rendre le template 'files.html' avec les données JSON
    with open("config.json") as f:
        config = json.load(f)
    filesshortshtml = "" 
    count = 0
    for name, link in config["filesShorts"].items():
        count += 1
        filesshortshtml += f'<div class="col-md-4"><a href="/files/{link}" class="btn btn-primary btn-block">{name}</a></div>'
        if count % 3 == 0:
            filesshortshtml += '<br style="margin-top: 50px;">'

    return render_template('files.html', files_data=files_data, buttons = filesshortshtml, defaultFile = config["defaultFile"])








@FILES.route('/files/<path:directory_path>')
def get_files_data(directory_path):
    if 'user' not in session:
        return redirect("/login")
    # Vérifier si le chemin spécifié existe et est un répertoire
    if not os.path.isdir(directory_path):
        return jsonify({'error': 'Le chemin spécifié n\'existe pas ou n\'est pas un répertoire.'}), 404

    files_data = []

    # Parcourir les fichiers et répertoires dans le dossier actuel
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        # Ignorer les fichiers commençant par un point (cachés)
        if not filename.startswith('.'):
            if os.path.isdir(file_path):
                # Si c'est un répertoire, ajouter ses informations
                files_data.append({
                    'name': filename,
                    'type': 'directory'
                })
            else:
                # Si c'est un fichier, ajouter ses informations
                files_data.append({
                    'name': filename,
                    'type': 'file',
                    'size': os.path.getsize(file_path)  # Taille du fichier en octets
                })

    # Rendre le template 'files.html' avec les données JSON
    with open("config.json") as f:
        config = json.load(f)
    filesshortshtml = "" 
    count = 0
    for name, link in config["filesShorts"].items():
        count += 1
        filesshortshtml += f'<div class="col-md-4"><a href="/files/{link}" class="btn btn-primary btn-block">{name}</a></div>'
        if count % 3 == 0:
            filesshortshtml += '<br style="margin-top: 50px;">'

    return render_template('files.html', files_data=files_data, buttons = filesshortshtml, defaultFile = config["defaultFile"])




@FILES.route('/fileview/<path:file_path>')
def fileview(file_path):
    if 'user' not in session:
        return redirect("/login")
    # Vérifier si le chemin spécifié existe et est un fichier
    if not os.path.isfile(file_path):
        return jsonify({'error': 'Le chemin spécifié n\'existe pas ou n\'est pas un fichier.'}), 404

    # Lire le contenu du fichier ligne par ligne
    with open(file_path, 'r') as file:
        file_content = file.read()
    file_content = file_content.replace("\n", "<br>")

    # Rendre le template 'fileview.html' avec le contenu du fichier
    return file_content