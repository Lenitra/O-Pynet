# Description: Install O-Pynet


cd ~

sudo rm -rf O-Pynet
git clone https://github.com/Lenitra/O-Pynet.git

cd O-Pynet

sudo pip install -r requirements.txt
pip install -r requirements.txt

# add to the crontab the command : @reboot sudo python3 /home/O-Pynet/main.py

crontab -l | { cat; echo "@reboot bash ~/O-Pynet/start.sh &"; } | crontab -
