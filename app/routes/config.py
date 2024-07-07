from flask import Blueprint, session, redirect, render_template, request


CONFIG = Blueprint("config", __name__)

# render template config
@CONFIG.route("/config")
def config():
    if "user" not in session:
        session["redirect"] = "config"
        return redirect("/login")
    
    return render_template("config.html")
