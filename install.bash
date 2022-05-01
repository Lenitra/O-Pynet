
echo "Installation des outils pour l'environement (git, python3, pip)"

sudo apt install git -y
sudo apt install python3 -y
sudo apt install python3-pip -y

echo "Téléchargement de OPyNet"
git clone https://github.com/Lenitra/O-Pynet.git
cd O-Pynet;
pip install -r requirements.txt


echo "Installation de OPyNet"

crontab -l > mycron
echo "@reboot bash /home/ubuntu/O-Pynet/src/start.sh" >> mycron
echo "@reboot bash /home/ubuntu/O-Pynet/src/loop.sh" >> mycron
crontab mycron
rm mycron

echo "Installation terminée redémarrage de la machine"

rm install.bash
sudo reboot