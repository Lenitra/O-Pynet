from flask import Blueprint, render_template, request, redirect, session
import json

LOGIN = Blueprint('login', __name__)


# Page de connexion
@LOGIN.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('user', None)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open("config.json") as f:
            config = json.load(f)
        for u, val in config["users"].items():
            if u == username and val["password"] == password:
                session['user'] = username
                if 'redirect' in session and session['redirect'] != "":
                    return redirect(f"/{session['redirect']}")
                return redirect(f"/dashboard")
    return render_template("login.html")