#!/bin/sh

crontab -l > mycron
echo "@reboot bash /home/ubuntu/O-Pynet/src/start.sh" >> mycron
crontab mycron
rm mycron

crontab -l > mycron
echo "@reboot bash /home/ubuntu/O-Pynet/src/loop.sh" >> mycron
crontab mycron
rm mycron

sudo reboot
