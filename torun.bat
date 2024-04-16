@REM Supprime le répertoire O-Pynet
rmdir /s /q O-Pynet

@REM Installe la dernière version de O-Pynet
git clone https://github.com/Lenitra/O-Pynet.git

@REM Récupère l'ancien fichier de configuration
move /tempopyconfig.json O-Pynet/config.json

@REM Passe sur le répertoire O-Pynet
cd O-Pynet

@REM Exécute le programme
python main.py