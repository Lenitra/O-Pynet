@REM passe sur le répertoire parent
cd ..

@REM déplace le fichier de configuration 
move O-Pynet/config.json /tempopyconfig.json

@REM déplace le fichier de lancement
move O-Pynet/torun.bat /supprime-moi.bat

@REM exécute le fichier de lancement
start ./supprime-moi.bat

