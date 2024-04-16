@REM move config.json to ../config.json
cd ..
move O-Pynet/config.json /tempopyconfig.json
@REM delete O-Pynet folder
rmdir /s /q O-Pynet
git clone https://github.com/Lenitra/O-Pynet.git
move /tempopyconfig.json O-Pynet/config.json
cd O-Pynet
python main.py