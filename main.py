
from flask import Flask, render_template, request, redirect, session
import psutil
import json
import os
from datetime import datetime


app = Flask(__name__)
app.secret_key = "ahcestcontulaspas"
app.debug = True




ROOT_DIR = os.path.abspath(os.path.dirname(__file__))


@app.route('/files')
def files():
    # Liste des fichiers dans le répertoire racine
    files = os.listdir(ROOT_DIR)
    # Filtre les répertoires
    directories = [f for f in files if os.path.isdir(os.path.join(ROOT_DIR, f))]
    # Filtre les fichiers
    files = [f for f in files if os.path.isfile(os.path.join(ROOT_DIR, f))]
    return render_template('files.html', directories=directories, files=files)

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
    return render_template("dashboard.html", refresh = refresh)





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


@app.route("/update", methods=['GET'])
def update():
    if 'user' not in session:
        return redirect("/login")
    os.system("move /y update.bat ..\\update.bat")
    os.system("start /b ..\\update.bat")




if __name__ == '__main__':
    STARTTIME = datetime.now()
    with open("config.json") as f:
        config = json.load(f)
    app.run(host=config["host"], port=config["port"])