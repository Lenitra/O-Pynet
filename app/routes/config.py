from flask import Blueprint, session, redirect, render_template, request


CONFIG = Blueprint("config", __name__)

# render template config
@CONFIG.route("/config")
def config():
    if "user" not in session:
        session["redirect"] = "config"
        return redirect("/login")
    
    return render_template("config.html")


@CONFIG.route("/config/save", methods=["POST", "GET"])
def save():
    if "user" not in session:
        session["redirect"] = "config"
        return redirect("/login")
    # get data from form
    data = request.form
    # save data
    # with open("config.json", "w") as f:
    #     f.write(str(data))
    print(data)
    return redirect("/config")

