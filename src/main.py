#!/usr/bin/python
# -*- coding: Utf-8 -*-
import platform
import os
from datetime import date, datetime
import socket
import sys
from flask import Flask, render_template, request, redirect, session
from matplotlib.pyplot import title
import yaml
import psutil

app = Flask(__name__)
app.secret_key = "ahcestcontulaspas"
app.debug = True


# Permet de charger la configration de la machine (appelée dans le main)
def loadconfig():
    # read the config file
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    return config

def is_logged():
    try:
        if session['is_logged'] == True:
            return True
    except:
        pass
    return redirect('/login')

def cmd(cmd):
    os.system(cmd)


@app.route('/')
def index():
    return render_template('index.html', title=config["title"])


@app.route('/reload')
def reload():
    # restart the server
    cmd("sudo reboot")
    return redirect('/dashboard')

@app.route('/login', methods=['GET', 'POST'])
def login():
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
                session['username'] = user
                session['is_logged'] = True
                return redirect('/dashboard')
    return redirect('/login')

@app.route('/rcdn')
def rcdn():
    ram = f"RAM : {round(psutil.virtual_memory()[3]/1000000000, 2)} / {round(psutil.virtual_memory()[0]/1000000000, 2)} Go | {psutil.virtual_memory()[2]}%"
    cpu = f"CPU : {psutil.getloadavg()[2]} / {os.cpu_count()}  | {(psutil.getloadavg()[2]/os.cpu_count()) * 100}%"
    disk = f"DISK : {round(psutil.disk_usage('/')[2]/1000000000, 2)} / {round(psutil.disk_usage('/')[0]/1000000000, 2)} Go | {psutil.disk_usage('/')[3]}%"
    network = f"NETWORK : download {round(psutil.net_io_counters()[1]/1000000000, 2)} Go \n upload {round(psutil.net_io_counters()[0]/1000000000, 2)} Go"
    return render_template('rcdn.html', config=config, ram=ram, cpu=cpu, disk=disk, network=network)


@app.route("/dashboard")
def dashboard():
    # print(session["is_logged"])
    if is_logged() != True:
        return is_logged()
    return render_template('dashboard.html', config=config)

    


if __name__ == '__main__':
    config = loadconfig()
    config["url"] = IP_addres = socket.gethostbyname(socket.gethostname()) + ":" + str(config["port"])

    # if platform.system() != "Windows":
    website_url = config["url"] 
    app.config['SERVER_NAME'] = website_url

    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SESSION_COOKIE_NAME'] = "BonsCookies"
    app.run()
