from flask import Blueprint, redirect, session, render_template
import json
import os
import app.routes.api as api

DASHBOARD = Blueprint('dashboard', __name__)


# Rediriger vers le login ou le tableau de bord
@DASHBOARD.route('/')
def index():
    if api.checks(["login"]):
        return api.checks(["login"])
    return render_template("dashboard.html")


# Affichage du tableau de bord
@DASHBOARD.route('/dashboard')
def dashboard():
    if api.checks(["login"]):
        return api.checks(["login"])

    with open("config.json") as f:
        config = json.load(f)

    return render_template("dashboard.html")


# Redémarrer la machine
@DASHBOARD.route('/reboot')
def reboot():
    if api.checks(["login", "reboot"]):
        return api.checks(["login", "reboot"])
    os.system("shutdown /r /f /t 0")
    os.system("sudo reboot")
    return redirect("/dashboard")
