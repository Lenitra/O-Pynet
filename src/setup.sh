#!/bin/sh

# add "@reboot bash O-Pynet/src/start.sh" to crontab
# Get crontab
crontab -l > mycron
# Append new cron into cron file
echo "@reboot bash /home/ubuntu/O-Pynet/src/start.sh" >> mycron
# Install new cron file
crontab mycron
rm mycron

