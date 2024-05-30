import base64
import time
import webbrowser
from flask import Blueprint, render_template, session, redirect, request, jsonify
import json
import subprocess 
import shutil 
import requests
import os

with open('access_token.txt', 'w') as f:
    f.write('')
    
SPOTIFY = Blueprint('spotify', __name__)

@SPOTIFY.route('/musique')
def spotify():
    if 'user' not in session:
        return redirect("/login")
    return render_template("spotify.html")





@SPOTIFY.route('/spotify/start')
def startSoftwareSpotify():
    os.system("spotify &")
    
    # try:
    # # Lancer Spotify via le shell
    #     subprocess.run("spotify &", shell=True, check=True)
    #     print("Spotify lancé avec succès.")
    # except subprocess.CalledProcessError as e:
    #     print(f"Erreur lors du lancement de Spotify : {e}")
    # except FileNotFoundError as e:
    #     print(f"Commande introuvable : {e}")
    
    spotify_path = shutil.which("spotify")

    if spotify_path:
        try:
            # Lancer Spotify
            subprocess.run([spotify_path], check=True)
            print("Spotify lancé avec succès.")
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors du lancement de Spotify : {e}")
    else:
        print("Spotify n'a pas été trouvé dans le PATH.")
    
    
    return "OK", 200



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
        'redirect_uri': "http://" + config["host"]+ ":" + config["port"] + '/spotify/callback',
    }
    response = requests.post(token_url, headers=headers, data=data)
    token_info = response.json()
    return token_info.get('access_token')



@SPOTIFY.route('/spotify/callback')
def callback():
    code = request.args.get('code')
    print("Le code expirera dans : ", request.args.get('expires_in'), " secondes")
    access_token = get_access_token(code)
    # save the access_token in a file
    with open('access_token.txt', 'w') as f:
        f.write(access_token)
    if access_token:
        # Vous pouvez effectuer d'autres actions ici, comme enregistrer le jeton d'accès dans une base de données
        return "Jetons d'accès obtenu avec succès!<br>"+access_token+"<script>setTimeout(function(){window.close();}, 1);</script>"
    else:
        return "Impossible d'obtenir le jeton d'accès."
    
    
    
@SPOTIFY.route('/spotify/getkey', methods=['GET' , 'POST'])
def login():
    with open('config.json') as f:
        config = json.load(f)
    client_id = config['spotify']['client_id']
    redirect_uri = "http://" + config["host"]+ ":" + config["port"] + '/spotify/callback'
    # Remplacez les scopes par ceux que vous souhaitez demander à l'utilisateur
    scope = 'user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming '
    state = 'some_state_value'  # Vous pouvez générer un état aléatoire ici si nécessaire
    authorize_url = 'https://accounts.spotify.com/authorize?' + \
                    'response_type=code&client_id=' + client_id + \
                    '&scope=' + scope + \
                    '&redirect_uri=' + redirect_uri + \
                    '&state=' + state
    return redirect(authorize_url)
    
    
    
@SPOTIFY.route('/musique/addqueue', methods=['POST'])
def addqueue():
    # Récupérer le jeton d'accès
    with open('access_token.txt', 'r') as f:
        access_token = f.read()
    with open('config.json') as f:
        config = json.load(f)
    headers = {'Authorization': 'Bearer ' + access_token}
    uri = request.args.get('uri')
    response = requests.post(f'https://api.spotify.com/v1/me/player/queue?uri={uri}', headers=headers)
    if response.status_code != 204:
        webbrowser.open('http://'+config["host"]+':'+config["port"]+'/spotify/getkey')
        time.sleep(3)
        requests.post(f'http://' + config["host"] + ':' + config["port"] + '/musique/addqueue?uri=' + uri)
    return "OK", 200


