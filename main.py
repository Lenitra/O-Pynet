#!/usr/bin/python
# -*- coding: Utf-8 -*-
import platform
import os
import random
import shutil
import time
from flask import Flask, render_template, request, redirect, session, send_file
import yaml
import requests
import psutil
from datetime import datetime


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
    

def loadphotosForHtml():
    if not os.path.exists(config["photosfolder"]):
        # create a folder photos in the directory ~
        try:
            os.system(f"mkdir {config['photosfolder']}")
        except:
            pass
        
    # copy all contnent recursively from the directory photos to the directory static/photos
    try:
        shutil.rmtree("static/photos")
        os.system("rm -rf static/photos")
    except:
        pass
    
    try:
        os.system(f"cp -r {config['photosfolder']} static/photos")
    except:
        pass

    





@app.route('/')
def index():
    return redirect("/dashboard")


@app.route('/reload')
def reload():
    # run sudo reboot
    os.system("sudo reboot")
    return redirect('/dashboard')


# @app.route('/update')
# def update():
#     os.system("pwd")
#     os.system("git config --global --add safe.directory /home/ubuntu/O-Pynet")
#     os.system("git pull")
#     return redirect('/dashboard')



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
    tmpcup = psutil.getloadavg()[2]
    # enlever tout ce qui 2 chiffres après la virgule
    tmpcup = round(tmpcup, 2)
    cpu = f"{tmpcup},{os.cpu_count()}"
    disk = f"{round(psutil.disk_usage('/')[2]/1000000000, 2)},{int(round(psutil.disk_usage('/')[0]/1000000000, 0))}"
    return render_template('rcdn.html', config=config, ram=ram, cpu=cpu, disk=disk)


@app.route("/dashboard")
def dashboard():
    if checkperms("log") != True:
        return redirect('/login')
    return render_template('dashboard.html', config=config)

@app.route("/updateopy")
def update():
    if checkperms("log") != True:
        return redirect('/login')
    # copy the directory conf to 555conf555
    try:
        shutil.copytree("conf", "../555conf555")
    except:
        shutil.rmtree("../555conf555")
        os.system("rm -rf ../555conf555")
        shutil.copytree("conf", "../555conf555")
    
    # shutil.rmtree("conf")
    os.system("rm -rf conf")
    
    # delete all files in the directory O-Pynet
    os.system("git config --global --add safe.directory /home/ubuntu/O-Pynet")
    os.system("sudo git pull")
    time.sleep(5)
    # copy the file conf and all files inside it
    shutil.rmtree("conf")
    os.system("rm -rf conf")

    shutil.copytree("../555conf555", "conf")

    shutil.rmtree("../555conf555")
    os.system("rm -rf ../555conf555")
    return redirect('/dashboard')




@app.route("/configupdate", methods=['POST', 'GET'])
def configupdate():
    if checkperms("log") != True:
        return redirect('/login')
    config["title"] = request.form['title']
    # config["default_folder"] = request.form['default_folder']
    config["port"] = int(request.form['port'])
    config["ramcputime"] = int(request.form['ramcputime'])
    saveconfig(config)
    time.sleep(5)
    try:
        if request.form['reboot'] != None:
            os.system("sudo reboot")
    except:
        pass
    return redirect('/dashboard')

@app.route("/config")
def param():
    if checkperms("log") != True:
        return redirect('/login')
    return render_template('config.html', config=config)



@app.route("/photos", methods=['POST', 'GET'])
def photo():
    if checkperms("log") != True:
        return redirect('/login')
    # get all folders in the directory photos
    listfolders = os.listdir(config["photosfolder"])

    html = ""
    for folder in listfolders:
        html += f"<a href='/photos/{folder}'>{folder}</a>"

    return render_template('photos.html', config=config, photos=html)



@app.route("/photos/<folder>", methods=['POST', 'GET'])
def photos(folder):
    if checkperms("log") != True:
        return redirect('/login')
    # get all photos in the folder
    listphotos = os.listdir(f"{config['photosfolder']}/{folder}")
    html = ""
    for photo in listphotos:
        html += "<div class='photo'>"
        html += f"<a href='/static/photos/{folder}/{photo}' class='photo'><img src='/static/photos/{folder}/{photo}'></a><a class='deletelink' href='/deletephoto/{folder}/{photo}'>X</a>"
        html += "</div>"
    return render_template('photofile.html', config=config, photos=html, folder=folder)


@app.route("/deletephoto/<folder>/<photo>")
def deletephoto(folder, photo):
    if checkperms("log") != True:
        return redirect('/login')
    os.remove(f"{config['photosfolder']}/{folder}/{photo}")
    loadphotosForHtml()
    return redirect(f'/photos/{folder}')


@app.route("/addfolder", methods=['POST', 'GET'])
def addfolder():
    if checkperms("log") != True:
        return redirect('/login')
    # get the name of the text field
    folder = request.form['foldername']
    # create the folder
    os.mkdir(f"{config['photosfolder']}/{folder}")
    loadphotosForHtml()
    return redirect('/photos')

@app.route("/addphoto/<folder>", methods=['POST', 'GET'])
def addphoto(folder):
    if checkperms("log") != True:
        return redirect('/login')
    # get all files form the form
    files = request.files.getlist('file[]')
    # save all files
    for file in files:
        file.save(f"{config['photosfolder']}/{folder}/{file.filename}")

    loadphotosForHtml()
    return redirect(f'/photos/{folder}')



@app.route("/dlallphotos")
def dlallphotos():
    # télécharger toutes les photos
    shutil.make_archive("photos", 'zip', "static/photos")
    return send_file("photos.zip", as_attachment=True)

@app.route("/dlfolder/<folder>")
def dlphotos(folder):
    # télécharger toutes les photos
    shutil.make_archive("photos", 'zip', f"static/photos/{folder}")
    return send_file("photos.zip", as_attachment=True)





if __name__ == '__main__':
    config = loadconfig()
    loadphotosForHtml()


    config["url"] = IP_addres = str(config["ip"]) + ":" + str(config["port"])

    if platform.system() != "Windows":
        website_url = config["url"] 
        app.config['SERVER_NAME'] = website_url

    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SESSION_COOKIE_NAME'] = "BonsCookies"
    print("Your admin panel is ready here : http://" + config["ip"] + ":" + str(config["port"]))
    
    # debug
    # app.config['SERVER_NAME'] = None 
    
    
    app.run()
