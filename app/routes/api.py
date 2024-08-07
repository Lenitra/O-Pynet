import json
from flask import Blueprint, request, redirect, session, render_template
from datetime import datetime
from app.aaa import format_size
import psutil
import app.aaa as aaa

# Heure de démarrage du serveur
STARTTIME = datetime.now()

API = Blueprint('api', __name__)


# Retourne l'utilisation du processeur
@API.route('/api/cpu', methods=['GET'])
def cpu():
    cpu = psutil.cpu_percent(interval=1, percpu=False)
    return {"cpu": cpu}


# Retourne l'utilisation de la RAM
@API.route('/api/memory', methods=['GET'])
def memory():
    memory = psutil.virtual_memory().percent
    return {"memory": memory}


# Retourne l'utilisation des différents disques de stockage
@API.route('/api/disk', methods=['GET'])
def disk():
    # lister tous les disques
    disk = []
    for part in psutil.disk_partitions():
        if "loop" in part.device:
            continue
        already = False
        for diskpart in disk:
            if diskpart["device"] == part.device:
                already = True
                break
        if already:
            continue
        #  ne pas afficher les disques à moins de 2.5go
        if psutil.disk_usage(part.mountpoint).total > 2500000000:
            psutil.disk_usage(part.mountpoint).total
            disk.append({"device": part.device, "usage": psutil.disk_usage(part.mountpoint).percent, "details": f"{format_size(psutil.disk_usage(part.mountpoint).used)} / {format_size(psutil.disk_usage(part.mountpoint).total)}"})
    return {"disk": disk}


# Retourne le temps de fonctionnement du serveur
@API.route('/api/uptime', methods=['GET'])
def uptime():
    uptime = datetime.now() - STARTTIME
    return {"uptime": str(uptime)}

@API.route('/api/configs', methods=['GET'])
def configs():
    with open("config.json") as f:
        config = json.load(f)
    return config

@API.route('/api/saveconfigs', methods=['GET', 'POST'])
def saveconfigs():
    print(request.json)

    toreg = request.json
    with open("config.json") as f:
        config = json.load(f)

    for key, value in config.items():
        if key not in toreg:
            toreg[key] = value

    with open("config.json", "w") as f:
        json.dump(toreg, f)
    aaa.wirteCommonJS()
    return {"status": "ok"}


# @arg tocheck: list of permissions to check
# list of checks : login, module-config, module-files, module-spotify, module-camera, reboot
# @return: None if all permissions are ok, redirect to error page if not
def checks(tocheck):
    for e in tocheck:
        if e == "login":
            if "user" not in session:
                return redirect("/login")

        with open("config.json") as f:
            config = json.load(f)

        if session["user"] not in config["users"]:
            return redirect("/login")

        permissions = config["users"][session["user"]]["permissions"]

        if e == "module-config" and not permissions.get("config", False):
            return redirect("/error?code=403")

        if e == "module-files" and not permissions.get("files", False):
            return redirect("/error?code=403")

        if e == "module-spotify" and not permissions.get("spotify", False):
            return redirect("/error?code=403")

        if e == "module-camera" and not permissions.get("camera", False):
            return redirect("/error?code=403")

        if e == "reboot" and not permissions.get("reboot", False):
            return redirect("/error?code=403")
        
    return None


