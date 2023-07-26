# Description: Install O-Pynet


cd ~;sudo rm -rf O-Pynet;git clone https://github.com/Lenitra/O-Pynet.git;cd O-Pynet;sudo pip install -r requirements.txt;pip install -r requirements.txt;crontab -l | { cat; echo "@reboot cd ~/O-Pynet;bash start.sh &"; } | crontab -; mkidr ~/photos;sudo reboot;
