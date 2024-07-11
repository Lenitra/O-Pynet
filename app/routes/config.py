from flask import Blueprint, session, redirect, render_template, request
import app.routes.api as api

CONFIG = Blueprint("config", __name__)

# render template config
@CONFIG.route("/config")
def config():
    if api.checks(["login", "module-config"]):
        return api.checks(["login", "module-config"])    
    return render_template("config.html")
