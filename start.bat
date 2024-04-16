@REM passe sur le répertoire parent
cd ..

@REM déplace le fichier de configuration 
move -Force O-Pynet/config.json tempopyconfig.json

@REM déplace le fichier de lancement
move -Force O-Pynet/torun.bat torun.bat

@REM exécute le fichier de lancement
start ./torun.bat

