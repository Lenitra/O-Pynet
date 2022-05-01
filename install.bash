
echo "Installation des outils pour l'environement (apt, git, python3, pip)"
sudo apt -y update
sudo apt-get -y install git 
sudo apt-get -y install python3
sudo apt-get -y install python3-pip

echo "Téléchargement de OPyNet"
git clone https://github.com/Lenitra/O-Pynet.git
cd O-Pynet;
pip install -r requirements.txt


echo "Installation de OPyNet"

crontab -l > mycron
echo "@reboot bash /home/ubuntu/O-Pynet/start.sh" >> mycron
echo "@reboot bash /home/ubuntu/O-Pynet/loop.sh" >> mycron
crontab mycron
rm mycron

echo "Installation terminée redémarrage de la machine"

rm install.bash
sudo reboot