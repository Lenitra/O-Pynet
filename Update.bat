@REM déplace le fichier de configuration 
move /y O-Pynet\config.json tempopyconfig.json

rmdir /s /q O-Pynet\

git clone https://github.com/Lenitra/O-Pynet.git

@REM Supprime le fichier O-Pynet\install.bat
del O-Pynet\install.bat

move /y tempopyconfig.json O-Pynet\config.json

move /y O-Pynet\start.bat start.bat 

move /y O-Pynet\update.bat update.bat
