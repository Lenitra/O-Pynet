#!/usr/bin/python
# -*- coding: Utf-8 -*-
import platform
import os
import random
import shutil
import time
from flask import Flask, render_template, request, redirect, session
import yaml
import requests
import psutil
from instabot import Bot

app = Flask(__name__)
app.secret_key = "ahcestcontulaspas"
app.debug = True


def get_current_ipv4():
    try:
        ip = requests.get("https://api4.ipify.org", timeout=10).text
        print(ip)
        return ip
    except requests.exceptions.ConnectionError as ex:
        return None


# Permet de charger la configration de la machine (appelée dans le main)
def loadconfig():
    # read the config file
    with open('conf/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    config["ip"] = get_current_ipv4()
    with open('conf/config.yaml', 'w') as file:
        config = yaml.dump(config, file)
    with open('conf/config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    return config

def saveconfig(config):
    with open('conf/config.yaml', 'w') as file:
        config = yaml.dump(config, file)


def checkperms(perm):
    if perm == "log":
        try:
            session['is_logged']
        except:
            return redirect("/login")
        if session['is_logged'] != True:
            return redirect("/login")
        return True
    

@app.route('/')
def index():
    return redirect("/dashboard")


@app.route('/reload')
def reload():
    # restart the server
    os.popen("sudo reboot")
    return redirect('/dashboard')


@app.route('/update')
def update():
    os.system("pwd")
    os.system("git config --global --add safe.directory /home/ubuntu/O-Pynet")
    os.system("git pull")
    return redirect('/dashboard')


@app.route('/graph')
def graph():
    # read the config file
    with open('tmp/drcdata.yaml', 'r') as f:
        data = yaml.safe_load(f)
    cpu = ''
    ram = ''
    disk = ''
    for k, v in data["cpu"].items():
        cpu += str(k) + ":" + str(v) + ","

    for k,v in data["ram"].items():
        ram += str(k) + ":" + str(v) + ","

    for k, v in data["disk"].items():
        disk += str(k) + ":" + str(v) + ","

    return render_template('graph.html', config = config, cpu=cpu, ram=ram, disk=disk)


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        del session["user"]  
        del session["is_logged"]
    except:
        pass
    return render_template('login.html', config=config)


@app.route('/checklogin', methods=['GET', 'POST'])
def checklogin():
    user = request.form['username']	
    password = request.form['password']
    with open('conf/accounts.yaml', 'r') as file:
        accounts = yaml.safe_load(file)
        for account in accounts:
            print(account)
            if account['user'] == user and account['password'] == password:
                session['user'] = user
                session['is_logged'] = True
                return redirect('/dashboard')
    return redirect('/login')


@app.route('/rcdn')
def rcdn():
    if checkperms("log") != True:
        return redirect('/login')
    ram = f"{round(psutil.virtual_memory()[3]/1000000000, 2)},{int(round(psutil.virtual_memory()[0]/1000000000, 0))}"
    cpu = f"{psutil.getloadavg()[2]},{os.cpu_count()}"
    disk = f"{round(psutil.disk_usage('/')[2]/1000000000, 2)},{int(round(psutil.disk_usage('/')[0]/1000000000, 0))}"
    return render_template('rcdn.html', config=config, ram=ram, cpu=cpu, disk=disk)


@app.route("/dashboard")
def dashboard():
    if checkperms("log") != True:
        return redirect('/login')
    session["console"] = ""
    session['dir'] = config['default_folder']
    return render_template('dashboard.html', config=config)





@app.route("/configupdate", methods=['POST', 'GET'])
def configupdate():
    if checkperms("log") != True:
        return redirect('/login')
    config["title"] = request.form['title']
    config["default_folder"] = request.form['default_folder']
    config["port"] = int(request.form['port'])
    config["ramcputime"] = int(request.form['ramcputime'])
    saveconfig(config)
    os.system("sudo reboot")
    return redirect('/dashboard')

@app.route("/config")
def param():
    if checkperms("log") != True:
        return redirect('/login')
    return render_template('config.html', config=config)



# region Insta

@app.route('/insta')
def insta():
    if checkperms("log") != True:
        return redirect('/login')
    try:

        img = os.listdir('static/insta/uncheck/')[0]
    except:
        img = None
    return render_template("insta.html", config=config, img=img)


@app.route('/getimgs')
def getimgs():
    if checkperms("log") != True:
        return redirect('/login')
    try:
        with open('static/insta/uncheck/page.html', 'r', encoding="utf_8") as file:
            html = file.read()
        for e in html.split('"'):
            if e.startswith("https://cdn.discordapp.com/attachments/"):
                if e.endswith(".jpg") or e.endswith(".png") or e.endswith("jepg"):
                    print(e)
                    img = requests.get(e)
                    with open("static/insta/uncheck/"+str(len(os.listdir('static/insta/uncheck/'))+1)+".jpg", 'wb') as f:
                        f.write(img.content)
    except:
        pass

    return redirect("/insta")


@app.route('/saveimg', methods=['POST', 'GET'])
def saveimg():
    if checkperms("log") != True:
        return redirect('/login')
    img = os.listdir('static/insta/uncheck/')[0]
    shutil.move("static/insta/uncheck/"+img, "static/insta/check/" +
                  str(len(os.listdir('static/insta/check/'))+1)+".jpg")
    return redirect("/insta")


@app.route('/delimg', methods=['POST', 'GET'])
def delimg():
    if checkperms("log") != True:
        return redirect('/login')
    img = os.listdir('static/insta/uncheck/')[0]
    os.remove("static/insta/uncheck/"+img)
    return redirect("/insta")



# endregion

if __name__ == '__main__':
    config = loadconfig()

    bot = Bot()

    config["url"] = IP_addres = str(config["ip"]) + ":" + str(config["port"])

    if platform.system() != "Windows":
        website_url = config["url"] 
        app.config['SERVER_NAME'] = website_url

    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SESSION_COOKIE_NAME'] = "BonsCookies"
    print("Your admin panel is ready here : http://" + config["ip"] + ":" + str(config["port"]))
    app.run()
