#!/usr/bin/python
# -*- coding: Utf-8 -*-
import platform
from datetime import date, datetime
import socket
from flask import Flask, render_template, request, redirect, session
import yaml

app = Flask(__name__)
app.secret_key = "ahcestcontulaspas"
app.debug = True


# Permet de charger la configration de la machine (appelée dans le main)
def loadconfig():
    pass


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


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
                return redirect('/admin')
    return redirect('/login')


@app.route("/admin")
def admin():
    return render_template('admin.html')


if __name__ == '__main__':
    loadconfig()
    # if platform.system() != "Windows":
    website_url = IP_addres = socket.gethostbyname(socket.gethostname()) + ":5000"
    app.config['SERVER_NAME'] = website_url

    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SESSION_COOKIE_NAME'] = "BonsCookies"
    app.run()
