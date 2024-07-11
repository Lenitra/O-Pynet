from flask import Blueprint, send_file, session, redirect, render_template, jsonify, send_file
import psutil
import json
import os
import app.routes.api as api

FILES = Blueprint('files', __name__)


@FILES.route('/download/<path:file_path>')
def download_file(file_path):
    if api.checks(["login", "module-files"]):
        return api.checks(["login", "module-files"])
    # Obtenir le chemin complet du fichier à télécharger
    full_path = os.path.join('./', file_path)

    # Vérifier si le fichier existe
    if os.path.isfile(full_path):
        # Envoyer le fichier au client pour téléchargement
        return send_file(full_path, as_attachment=True)
    else:
        return 'Le fichier spécifié n\'existe pas.', 404


# Afficher les différents répertoires de disques
@FILES.route('/files')
def get_discks():

    if api.checks(["login", "module-files"]):
        return api.checks(["login", "module-files"])

    # lister les disques
    files_data = []
    tmp_disk = []
    for part in psutil.disk_partitions():
        if "loop" in part.device:
            continue
        if part.device in tmp_disk:
            continue

        tmp_disk.append(part.device)

        files_data.append({
            'name': part.device.split("\\")[0],
            'type': 'directory'
        })

    # Gestion des raccourcis
    with open("config.json") as f:
        config = json.load(f)
    filesshortshtml = "" 
    count = 0
    for name, link in config["filesShorts"].items():
        count += 1
        filesshortshtml += f'<div class="col-md-4"><a href="/files/{link}" class="btn btn-primary btn-block">{name}</a></div>'
        if count % 3 == 0:
            filesshortshtml += '<br style="margin-top: 50px;">'

    return render_template('files.html', files_data=files_data, buttons = filesshortshtml)


@FILES.route('/files/<path:directory_path>')
def get_files_data(directory_path):

    if api.checks(["login", "module-files"]):
        return api.checks(["login", "module-files"])

    with open("config.json") as f:
        config = json.load(f)
    if config["os"] == "linux":
        directory_path = f"/{directory_path}"
    # Vérifier si le chemin spécifié existe et est un répertoire

    if not os.path.isdir(directory_path):
        return jsonify({
            'error': 'Le chemin spécifié n\'existe pas ou n\'est pas un répertoire.',
            "directory_path": directory_path
            }), 404

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

    # Gestion des raccourcis
    filesshortshtml = "" 
    count = 0
    for name, link in config["filesShorts"].items():
        count += 1
        filesshortshtml += f'<div class="col-md-4"><a href="/files/{link}" class="btn btn-primary btn-block">{name}</a></div>'
        if count % 3 == 0:
            filesshortshtml += '<br style="margin-top: 50px;">'

    return render_template('files.html', files_data=files_data, buttons = filesshortshtml)


@FILES.route('/fileview/<path:file_path>')
def fileview(file_path):

    if api.checks(["login", "module-files"]):
        return api.checks(["login", "module-files"])

    with open("config.json") as f:
        config = json.load(f)
    if config["os"] == "linux":
        file_path = f"/{file_path}"

    # Vérifier si le chemin spécifié existe et est un fichier
    if not os.path.isfile(file_path):
        return jsonify({'error': 'Le chemin spécifié n\'existe pas ou n\'est pas un fichier.', 
                        "file_path": file_path}), 404

    # Lire le contenu du fichier ligne par ligne
    with open(file_path, 'r') as file:
        file_content = file.read()
    file_content = file_content.replace("\n", "<br>")

    # Rendre le template 'fileview.html' avec le contenu du fichier
    return file_content
