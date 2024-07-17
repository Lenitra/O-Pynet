# O-Pynet
Panneau administratif pour serveur personnel

### Fonctionnalités
- Authentification 
- Affichage des ressources utilisées (CPU, RAM, Stockage)
- Bouton de redémarrage rapide
- Visualisation des fichiers
- Connexion à l'api spotify
- Camera de surveillance (experimental)

### Installation
Pour les utilisateurs sous Débian:
- Installez le package libgl1-mesa-glx (sudo apt-get install libgl1-mesa-glx)
- Installez les requirements (pip install -r requirements.txt)
- Exécutez le fichier main.py (python3 main.py) pour démarrer le projet

## Notes :
sudo usermod -aG video,sudo $USER
