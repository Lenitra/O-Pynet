#!/usr/bin/python
# -*- coding: Utf-8 -*-
import platform
import os
import re
from tabnanny import check
from flask import Flask, render_template, request, redirect, session
import yaml
import requests
import psutil

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
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    config["ip"] = get_current_ipv4()
    with open('config/config.yaml', 'w') as file:
        config = yaml.dump(config, file)
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    return config

def saveconfig(config):
    with open('config/config.yaml', 'w') as file:
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
    with open('config/accounts.yaml', 'r') as f:
        data = yaml.safe_load(f)
    for user in data:
        if session["user"] == user["user"]:
            if user["perms"][perm] == True:
                return True
    return redirect("/permerror")
    

def cmd(cmd):
    os.system("rm -rf tmp/tmp.sh")
    try :
        session["dir"]
    except:
        session['dir'] = "/home"

    with open('tmp/tmp.sh', 'w') as file:
        file.write(f"cd ~; \ncd {session['dir']}; \n{cmd};")
    return os.popen("bash tmp/tmp.sh").read()


@app.route('/')
def index():
    return render_template('index.html', title=config["title"])

@app.route('/graph')
def graph():
    # read the config file
    with open('tmp/usage.yaml', 'r') as f:
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



@app.route('/permerror')
def permerror():
    return render_template('permerror.html', config=config)

@app.route('/reload')
def reload():
    # restart the server
    cmd("sudo reboot")
    return redirect('/dashboard')


@app.route('/login', methods=['GET', 'POST'])
def login():
    del session["user"]  
    del session["is_logged"]
    return render_template('login.html', config=config)


@app.route('/checklogin', methods=['GET', 'POST'])
def checklogin():
    user = request.form['username']	
    password = request.form['password']
    with open('config/accounts.yaml', 'r') as file:
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

    
@app.route("/cmd", methods=['POST', 'GET'])
def cmd_exec():
    if checkperms("log") != True:
        return checkperms("log")
    if checkperms("cmd") != True:
        return checkperms("cmd")
    # Si il y a pas de commande valide (à la première connexion ou à l'envois d'un formulaire vide)
    try :
        command = request.form['cmd']
    except:
        command = False
    if command == "":
        command = False
    if type(command) != str:
        return render_template('cmd.html', config=config, console=session["console"], pwd=session["dir"])

    try:
        session["dir"]
    except:
        session['dir'] = config['default_folder']

    if command == "clear":
        session["console"] = ""
        torun = ""
    
    elif command.startswith("cd"):
        try :
            command.split(" ")[1]
            if command.split(" ")[1] == "~":
                session['dir'] = "/home"
            elif command.split(" ")[1] == "..":
                dire = session["dir"].split("/")
                dire[-1] = ""
                session["dir"] = "" 
                for e in dire:
                    session["dir"] += e + "/"
                session["dir"] = session["dir"][:-1]
                session["dir"] = session["dir"][:-1]
            else:
                session["dir"] += "/" + command.split(" ")[1]
                session["console"] += "\n> " + command + "\n" + session["dir"] + "\n"
            return render_template('cmd.html', config=config, console=session["console"], pwd=session["dir"])
        except:
            session["dir"] = config["default_folder"]
    else:
        torun = cmd(command)
        print(torun)



    try:
        session["console"] += "> " + command + "\n" + torun + "\n"
    except:
        session["console"] = torun
    return render_template('cmd.html', config=config, console=session["console"], pwd = session["dir"])


@app.route("/configupdate", methods=['POST', 'GET'])
def configupdate():
    if checkperms("log") != True:
        return redirect('/login')
    if checkperms("config") != True:
        return redirect('/permerror')
    config["title"] = request.form['title']
    config["default_folder"] = request.form['default_folder']
    config["port"] = int(request.form['port'])
    config["ramcputime"] = int(request.form['ramcputime'])
    saveconfig(config)
    cmd("sudo reboot")
    return redirect('/dashboard')

@app.route("/config")
def param():
    if checkperms("log") != True:
        return redirect('/login')
    return render_template('config.html', config=config)

if __name__ == '__main__':
    config = loadconfig()


    config["url"] = IP_addres = str(config["ip"]) + ":" + str(config["port"])

    if platform.system() != "Windows":
        website_url = config["url"] 
        app.config['SERVER_NAME'] = website_url

    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SESSION_COOKIE_NAME'] = "BonsCookies"
    print("Your admin panel is ready here : http://" + config["ip"] + ":" + str(config["port"]))
    app.run()
