from flask import Blueprint, redirect, session, render_template
import json
import os

DASHBOARD = Blueprint('dashboard', __name__)


# Rediriger vers le login ou le tableau de bord
@DASHBOARD.route('/')
def index():
    if 'user' in session:
        return redirect("/dashboard")
    return redirect("/login")



# Affichage du tableau de bord
@DASHBOARD.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect("/login")
    
    with open("config.json") as f:
        config = json.load(f)
    refresh = config["refresh"]*1000
    

        
    
    return render_template("dashboard.html", refresh = refresh)



# Redémarrer la machine
@DASHBOARD.route('/reboot')
def reboot():
    if 'user' not in session:
        return redirect("/login")
    os.system("shutdown /r /f /t 0")
    os.system("sudo reboot")
    return redirect("/dashboard")