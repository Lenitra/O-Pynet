cd ~;
sudo rm -rf O-Pynet;
git clone https://github.com/Lenitra/O-Pynet.git;
cd O-Pynet;
sudo pip install -r ~/O-Pynet/requirements.txt;
crontab -l | { cat; echo "@reboot cd ~/O-Pynet;bash start.sh &"; } | crontab -;
mkdir ~/photos;
sudo reboot;