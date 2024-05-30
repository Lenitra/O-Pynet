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
    
    html_liens = ""
    if len(config["liens"]) > 0:
        html_liens = '<div class="section"><h2>Liens</h2><div class="row">'
        for name, link in config["liens"].items():
            html_liens += f'<div class="col-md-6"><a href="{link}" class="btn btn-primary btn-block mb-2" target="_blank">{name}</a></div>'
        html_liens += '</div></div>'
        
    
    return render_template("dashboard.html", refresh = refresh, defaultFile = config["defaultFile"], liens = html_liens)



# Redémarrer la machine
@DASHBOARD.route('/reboot')
def reboot():
    if 'user' not in session:
        return redirect("/login")
    os.system("shutdown /r /f /t 0")
    os.system("sudo reboot")
    return redirect("/dashboard")