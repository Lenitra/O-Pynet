
cd ~
# copy the O-Pynet conf folder to the home directory named as 555temp555
cp -r O-Pynet/conf 555temp555
# copy this file to the home directory named as 555temp555.sh
# cp O-Pynet/start.sh 555temp555.sh
# run the 555temp555.sh file
# bash 555temp555.sh &
# remove the O-Pynet folder
rm 555temp555.sh
echo > 555temp555.sh

echo "echo 'O-Pynet is starting...';" >> 555temp555.sh
echo "cd ~;" >> 555temp555.sh

echo "echo 'Suppression de O-Pynet...';" >> 555temp555.sh
echo "rm -rf O-Pynet;" >> 555temp555.sh

echo "echo 'Clonage de O-Pynet...';" >> 555temp555.sh
echo "git clone https://github.com/Lenitra/O-Pynet.git;" >> 555temp555.sh

echo "echo 'Copie de la configuration...';" >> 555temp555.sh
echo "rm -rf O-Pynet/conf;" >> 555temp555.sh
echo "cp -r 555temp555 O-Pynet/conf;" >> 555temp555.sh
echo "rm -rf 555temp555;" >> 555temp555.sh

echo "echo 'Lancement de O-Pynet...';" >> 555temp555.sh
echo "cd O-Pynet;" >> 555temp555.sh
echo "sudo python3 main.py;" >> 555temp555.sh

cd ~
bash 555temp555.sh 
