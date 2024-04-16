@REM passe sur le répertoire parent
cd ..

@REM déplace le fichier de configuration 
move O-Pynet/config.json /tempopyconfig.json

@REM déplace le fichier de lancement
move O-Pynet/torun.bat /torun.bat

@REM exécute le fichier de lancement
start ./torun.bat

