
cd ~
# copy the O-Pynet conf folder to the home directory named as 555temp555
cp -r O-Pynet/conf 555temp555
# copy this file to the home directory named as 555temp555.sh
# cp O-Pynet/start.sh 555temp555.sh
# run the 555temp555.sh file
# bash 555temp555.sh &
# remove the O-Pynet folder
rm -rf O-Pynet
# clone the O-Pynet repository
git clone https://github.com/Lenitra/O-Pynet.git

# copy the conf folder to the O-Pynet folder
cp -r 555temp555 O-Pynet/conf
# remove the 555temp555 folder
rm -rf 555temp555

cd O-Pynet
sudo python3 main.py
