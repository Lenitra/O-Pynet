@REM move config.json to ../config.json
cd ..
move O-Pynet/config.json /tempopyconfig.json
move O-Pynet/torun.bat /torun.bat
@REM execute torun.bat in a new window
start torun.bat

