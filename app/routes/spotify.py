import base64
import platform
import time
import webbrowser
from flask import Blueprint, render_template, session, redirect, request, jsonify
import json
import subprocess 
import shutil 
import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

with open('access_token.txt', 'w') as f:
    f.write('')
    
    
SPOTIFY = Blueprint('spotify', __name__)

@SPOTIFY.route('/musique')
def spotify():
    if 'user' not in session:
        return redirect("/login")
    return render_template("spotify.html")


@SPOTIFY.route('/spotify/play', methods=['POST' , 'GET'])
def play():
    
    with open('config.json') as f:
        config = json.load(f)
        
    # Récupérer le jeton d'accès
    with open('access_token.txt', 'r') as f:
        access_token = f.read()
    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.put('https://api.spotify.com/v1/me/player/play', headers=headers)
    if response.status_code != 204:
        print(response.status_code)
        print(response.status_code)
        print(response.status_code)
        print(response.status_code)
        print(response.status_code)
        print(response.status_code)
        if response.status_code == 404:
            # Definir l'ordi comme device actif
            if requests.post('http://localhost:' + config["port"] + '/spotify/activatedevice').status_code == 200:
                time.sleep(0.5)
                requests.post('http://localhost:' + config["port"] + '/spotify/play')
            else:
                return "Spotify n'est pas ouvert sur l'ordinateur", 400
        
        elif response.status_code == 403:
            # musique déjà en cours de lecture
            return redirect("/musique")
            
        elif response.status_code == 401 or response.status_code == 400:
            os.system('firefox http://localhost:'+config["port"]+'/spotify/getkey')
            time.sleep(2)
            requests.post('http://localhost:' + config["port"] + '/spotify/play')
        else:
            print("Erreur inconnue")
            
    return redirect("/musique")


@SPOTIFY.route('/spotify/activatedevice', methods=['POST' , 'GET'])
def activatedevice():
        
    with open('access_token.txt', 'r') as f:
        access_token = f.read()
    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.get(f'https://api.spotify.com/v1/me/player/devices', headers=headers)
    # dans la liste récupérée, on cherche l'appareil qui a le nom donné
    device_name = platform.node()
    devices = response.json()['devices']
    device_id = None
    for device in devices:
        if device['name'] == device_name:
            device_id = device['id']
            break
    if device_id:
        data = {'device_ids': [device_id]}
        response = requests.put('https://api.spotify.com/v1/me/player', headers=headers, json=data)
        if response.status_code == 204:
            return "OK", 200
        else:
            return "Erreur", 400
    

@SPOTIFY.route('/spotify/pause', methods=['POST' , 'GET'])
def pause():
    with open('config.json') as f:
        config = json.load(f)
    # Récupérer le jeton d'accès
    with open('access_token.txt', 'r') as f:
        access_token = f.read()
    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.put('https://api.spotify.com/v1/me/player/pause', headers=headers)
    if response.status_code != 204:
        if response.status_code == 404:
            # Definir l'ordi comme device actif
            if requests.post('http://localhost:' + config["port"] + '/spotify/activatedevice').status_code == 200:
                time.sleep(0.5)
                requests.post('http://localhost:' + config["port"] + '/spotify/pause')
            else:
                return "Spotify n'est pas ouvert sur l'ordinateur", 400
        elif response.status_code == 403:
            # musique déjà en pause
            return redirect("/musique")
        elif response.status_code == 401 or response.status_code == 400:
            os.system('firefox http://localhost:'+config["port"]+'/spotify/getkey')
            time.sleep(2)
            requests.post('http://localhost:' + config["port"] + '/spotify/pause')
        else:
            print("Erreur inconnue")
    return redirect("/musique")


@SPOTIFY.route('/spotify/next', methods=['POST' , 'GET'])
def next():
    with open('config.json') as f:
        config = json.load(f)
    # Récupérer le jeton d'accès
    with open('access_token.txt', 'r') as f:
        access_token = f.read()
    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.post('https://api.spotify.com/v1/me/player/next', headers=headers)
    if response.status_code != 204:
        if response.status_code == 404:
            # Definir l'ordi comme device actif
            if requests.post('http://localhost:' + config["port"] + '/spotify/activatedevice').status_code == 200:
                time.sleep(0.5)
                requests.post('http://localhost:' + config["port"] + '/spotify/next')
            else:
                return "Spotify n'est pas ouvert sur l'ordinateur", 400
            
        elif response.status_code == 401 or response.status_code == 400:
            os.system('firefox http://localhost:'+config["port"]+'/spotify/getkey')
            time.sleep(2)
            requests.post('http://localhost:' + config["port"] + '/spotify/next')
        else:
            print("Erreur inconnue")
    return redirect("/musique")

# retourne les informations de la musique en cours de lecture et de la file d'attente
@SPOTIFY.route('/spotify/music-info', methods=['POST' , 'GET'])
def getinfos():
    with open('config.json') as f:
        config = json.load(f)
    # Récupérer le jeton d'accès
    with open('access_token.txt', 'r') as f:
        access_token = f.read()
    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.get('https://api.spotify.com/v1/me/player', headers=headers)
    
    toret = {}
    
    if response.status_code == 401 or response.status_code == 400:
        os.system('firefox http://localhost:'+config["port"]+'/spotify/getkey')
        
    if response.status_code == 200:
        item = response.json()['item']
        if item:
            infos = get_track_info(item['uri'])
            toret = {"title": infos[0], "artist": infos[1]}
    if toret == {}:
        toret = {"title": "Chargement...", "artist": "Chargement..."}
        
    return jsonify(toret)

@SPOTIFY.route('/spotify/search', methods=['POST' , 'GET'])
def search():
    with open('config.json') as f:
        config = json.load(f)
    champRecherche = request.args.get('nom_chanson')
    infos = recherche_chanson(champRecherche)
    return jsonify(infos)
    

# Fonction pour obtenir le jeton d'accès en échange du code d'autorisation
def get_access_token(code):
    with open('config.json') as f:
        config = json.load(f)
    client_id = config['spotify']['client_id']
    client_secret = config['spotify']['client_secret']
    token_url = 'https://accounts.spotify.com/api/token'
    headers = {'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode()).decode()}
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': "http://localhost:" + config["port"] + '/spotify/callback',
    }
    response = requests.post(token_url, headers=headers, data=data)
    token_info = response.json()
    return token_info.get('access_token')



@SPOTIFY.route('/spotify/callback', methods=['POST' , 'GET'])
def callback():
    code = request.args.get('code')
    access_token = get_access_token(code)
    # save the access_token in a file
    with open('access_token.txt', 'w') as f:
        f.write(access_token)
    if access_token:
        # Vous pouvez effectuer d'autres actions ici, comme enregistrer le jeton d'accès dans une base de données
        return "Jetons d'accès obtenu avec succès!<script>setTimeout(function(){window.close();}, 10);</script>"
    else:
        return "Impossible d'obtenir le jeton d'accès."
    
    
    
@SPOTIFY.route('/spotify/getkey', methods=['GET' , 'POST'])
def login():
    with open('config.json') as f:
        config = json.load(f)
    client_id = config['spotify']['client_id']
    redirect_uri = "http://localhost:" + config["port"] + '/spotify/callback'
    # Remplacez les scopes par ceux que vous souhaitez demander à l'utilisateur
    scope = 'user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming '
    state = 'some_state_value'  # Vous pouvez générer un état aléatoire ici si nécessaire
    authorize_url = 'https://accounts.spotify.com/authorize?' + \
                    'response_type=code&client_id=' + client_id + \
                    '&scope=' + scope + \
                    '&redirect_uri=' + redirect_uri + \
                    '&state=' + state
    return redirect(authorize_url)
    
    
    
@SPOTIFY.route('/musique/addqueue',methods=['POST' , 'GET'])
def addqueue():
    if 'user' not in session:
        return redirect("/login")
    # Récupérer le jeton d'accès
    with open('access_token.txt', 'r') as f:
        access_token = f.read()
    with open('config.json') as f:
        config = json.load(f)
    headers = {'Authorization': 'Bearer ' + access_token}
    uri = request.args.get('uri')
    response = requests.post(f'https://api.spotify.com/v1/me/player/queue?uri={uri}', headers=headers)
    if response.status_code != 204:
        webbrowser.open('http://localhost:'+config["port"]+'/spotify/getkey')
        time.sleep(3)
        requests.post(f'http://' + config["host"] + ':' + config["port"] + '/musique/addqueue?uri=' + uri)
    return "OK", 200







# region Spotify API Credentials
def recherche_chanson(nom_chanson):
    with open('config.json') as f:
        config = json.load(f)
    client_id = config['spotify']['client_id']
    client_secret = config['spotify']['client_secret']
    # Authentification avec les clés d'API
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    toret = None
    # Recherche de la chanson
    results = sp.search(q=nom_chanson, limit=1, type="track")
    
    elem = results["tracks"]["items"]
    toret = {"title": elem["name"], "artist": elem["artists"][0]["name"], "uri": elem["uri"], "img": elem["album"]["images"][0]["url"]}
    return toret
        





def get_track_info(uri):
    with open('config.json') as f:
        config = json.load(f)
    client_id = config['spotify']['client_id']
    client_secret = config['spotify']['client_secret']

    # Authentification avec les clés d'API
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    try:
        # Obtenir les informations sur la piste à partir de son URI
        track_info = sp.track(uri)

        # Extraire le nom du titre et le premier artiste
        if track_info:
            track_name = track_info["name"]
            artist_name = track_info["artists"][0]["name"]
            url = "https://open.spotify.com/track/" + uri.split(":")[-1]
            return track_name, artist_name, url
    except Exception as e:
        print("Erreur lors de la récupération des informations de la piste.")
        print(e)
        
    return None, None, None

# endregion