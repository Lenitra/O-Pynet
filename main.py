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
    

def loadphotos():
    # delete all photos in static/photos
    shutil.rmtree("static/photos")
    os.mkdir("static/photos")
    photos = os.listdir(config["photosfolder"])
    # copy all photos from photosfolder to static/photos
    for photo in photos:
        shutil.copyfile(f"{config['photosfolder']}/{photo}", f"static/photos/{photo}")


def trier_et_renommer_photos():
    dossier_photos = config["photosfolder"]
    # # Liste les fichiers du dossier
    fichiers = os.listdir(dossier_photos)
    try:
        os.mkdir(f"{dossier_photos}/tmp")
    except:
        shutil.rmtree(f"{dossier_photos}/tmp")

    # move all photos to tmp folder and convert them to jpg
    for fichier in fichiers:
        if fichier.endswith('.jpg'):
            shutil.move(f"{dossier_photos}/{fichier}", f"{dossier_photos}/tmp/{fichier}")
        elif fichier.endswith('.png') or fichier.endswith('.jpeg'):
            os.system(f"convert {dossier_photos}/{fichier} {dossier_photos}/tmp/{fichier}.jpg")
            os.remove(f"{dossier_photos}/{fichier}")

    fichiers = os.listdir(f"{dossier_photos}/tmp")
    # Filtrer uniquement les fichiers avec l'extension .jpg
    fichiers_jpg = [fichier for fichier in fichiers if fichier.endswith('.jpg')]

    # Trie les fichiers par date de création
    fichiers_tries = sorted(fichiers_jpg, key=lambda x: os.path.getctime(os.path.join(dossier_photos, x)))

    # Format de nommage pour les photos
    format_nom = "{:09d}.jpg"
    nouveau_nom = 0
    # Parcourir les fichiers triés et les renommer dans l'ordre croissant
    for fichier in fichiers_tries:
        # Récupère la date de création du fichier
        date_creation = datetime.fromtimestamp(os.path.getctime(os.path.join(dossier_photos, fichier)))

        # Formatte le nouveau nom en utilisant le format_nom
        nouveau_nom_formatte = format_nom.format(nouveau_nom)

        # Construit le nouveau chemin complet pour le fichier renommé
        nouveau_chemin = os.path.join(dossier_photos, nouveau_nom_formatte)

        # Renomme le fichier
        os.rename(os.path.join(dossier_photos, fichier), nouveau_chemin)

        # Incrémente le nouveau_nom pour le prochain fichier
        nouveau_nom += 1
    # delete all photos from tmp folder
    shutil.rmtree(f"{dossier_photos}/tmp")


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
    session["console"] = ""
    session['dir'] = config['default_folder']
    return render_template('dashboard.html', config=config)





@app.route("/configupdate", methods=['POST', 'GET'])
def configupdate():
    if checkperms("log") != True:
        return redirect('/login')
    config["title"] = request.form['title']
    # config["default_folder"] = request.form['default_folder']
    # config["port"] = int(request.form['port'])
    config["ramcputime"] = int(request.form['ramcputime'])
    saveconfig(config)
    if request.form['reboot'] != None:
        os.system("sudo reoboot")
    return redirect('/dashboard')

@app.route("/config")
def param():
    if checkperms("log") != True:
        return redirect('/login')
    return render_template('config.html', config=config)



@app.route("/photo/maul", methods=['POST', 'GET'])
def photo():
    if checkperms("log") != True:
        return redirect('/login')
    photos = os.listdir("static/photos")
    html = ""
    for photo in photos:
        if photo != "none":
            html += f'<a href="/static/photos/{photo}" target="_blank" class="flex-items"><img src="/static/photos/{photo}" width="100%"></a>'
    return render_template('photos.html', config=config, photos=html)


@app.route("/addphoto", methods=['POST', 'GET'])
def addphoto():
    if checkperms("log") != True:
        return redirect('/login')
    return render_template('addphoto.html', config=config)

@app.route("/savephotosended", methods=['POST', 'GET'])
def savephotosended():
    if checkperms("log") != True:
        return redirect('/login')


    print("------!TENTATIVE!-------")
    if 'fileToUpload' in request.files:
        print("------!UPLOAD!-------")
        files = request.files.getlist('fileToUpload')
        print(files)
        
        # Parcours les fichiers téléchargés
        for file in files:
            print(file)
            num = 0
            max_num = 0
            listdirphotos = os.listdir(config["photosfolder"])
            for photo in listdirphotos:
                filename = os.path.splitext(photo)[0]
                try:
                    num = int(filename)
                    max_num = max(max_num, num)
                except ValueError:
                    pass

            # Commencer à incrémenter à partir du plus grand numéro existant + 1
            num = max_num + 1

            file.save(os.path.join(config["photosfolder"], str(num)+"."+file.filename.split(".")[-1]))
            print("------!SAVED!-------")
            print("save as :" + str(num)+"."+file.filename.split(".")[-1])
            print("in :" + config["photosfolder"])
            loadphotos()

    return redirect('/photo/maul')

if __name__ == '__main__':
    config = loadconfig()
    trier_et_renommer_photos()
    loadphotos()


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
