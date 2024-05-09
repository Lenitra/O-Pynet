# Author: TauMah
from flask import Flask, jsonify, render_template, request, redirect, send_file, session
import psutil
import json
import os
from datetime import datetime
import subprocess

app = Flask(__name__)
app.secret_key = "ahcestcontulaspas"
app.debug = True







@app.route('/download/<path:file_path>')
def download_file(file_path):
    # Obtenir le chemin complet du fichier à télécharger
    full_path = os.path.join('./', file_path)

    # Vérifier si le fichier existe
    if os.path.isfile(full_path):
        # Envoyer le fichier au client pour téléchargement
        return send_file(full_path, as_attachment=True)
    else:
        return 'Le fichier spécifié n\'existe pas.', 404




@app.route('/files/<path:directory_path>')
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


@app.route('/fileview/<path:file_path>')
def fileview(file_path):
    if 'user' not in session:
        return redirect("/login")
    # Vérifier si le chemin spécifié existe et est un fichier
    if not os.path.isfile(file_path):
        return jsonify({'error': 'Le chemin spécifié n\'existe pas ou n\'est pas un fichier.'}), 404

    # Lire le contenu du fichier
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Rendre le template 'fileview.html' avec le contenu du fichier
    return file_content







def is_repo_up_to_date():
    try:
        # Run 'git fetch' command to update the remote-tracking branches
        subprocess.check_output(['git', 'fetch'])
        
        # Run 'git status' command to check the status of the repository
        output = subprocess.check_output(['git', 'status', '-uno'])
        
        # Check if the output contains the phrase 'Your branch is up to date'
        if b'Your branch is up to date' in output:
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        # Handle any errors that occur during the subprocess calls
        return False



# Redirection vers la page de login si l'utilisateur n'est pas connecté
@app.route('/')
def index():
    if 'user' in session:
        return redirect("/dashboard")
    return redirect("/login")


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('user', None)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open("config.json") as f:
            config = json.load(f)
        for u, p in config["users"].items():
            if u == username and p == password:
                session['user'] = username
                return redirect("/dashboard")
    return render_template("login.html")



@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect("/login")
    
    with open("config.json") as f:
        config = json.load(f)
    refresh = config["refresh"]*1000
    return render_template("dashboard.html", refresh = refresh, defaultFile = config["defaultFile"])





@app.route('/reboot')
def reboot():
    if 'user' not in session:
        return redirect("/login")
    os.system("shutdown /r /f /t 0")
    return redirect("/dashboard")

# API
@app.route('/api/cpu', methods=['GET'])
def cpu():
    cpu = psutil.cpu_percent(interval=1, percpu=False)
    return {"cpu": cpu}

@app.route('/api/memory', methods=['GET'])
def memory():
    memory = psutil.virtual_memory().percent
    return {"memory": memory}
    
@app.route('/api/disk', methods=['GET'])
def disk():
    # lister tous les disques
    disk = []
    for part in psutil.disk_partitions():
        disk.append({"device": part.device, "usage": psutil.disk_usage(part.mountpoint).percent})
    return {"disk": disk}

@app.route('/api/uptime', methods=['GET'])
def uptime():
    uptime = datetime.now() - STARTTIME
    return {"uptime": str(uptime)}






if __name__ == '__main__':
    STARTTIME = datetime.now()
    with open("config.json") as f:
        config = json.load(f)
    app.run(host=config["host"], port=config["port"])