@REM déplace le fichier de configuration 
move /y O-Pynet\config.json tempopyconfig.json

@REM Supprime le dossier O-Pynet
rmdir /s /q O-Pynet\

@REM Clone le dépôt
git clone https://github.com/Lenitra/O-Pynet.git

@REM Remet le fichier de configuration
move /y tempopyconfig.json O-Pynet\config.json

@REM Remet les fichiers de démarrage
move /y O-Pynet\start.bat start.bat 

@REM Remet le fichier de mise à jour
move /y O-Pynet\update.bat update.bat
