import os
import time
import psutil

import yaml


hour = -1
day = -1

while True: 
    # time.sleep(60)
    print("hour : " + str(hour))
    print("day : " + str(day))
    print("----")

    if day != time.localtime().tm_mday:
        day = time.localtime().tm_mday
        user = {"disk": {}, "ram": {}, "cpu": {}}
        with open('tmp/usage.yaml', 'w') as file:
            user = yaml.dump(user, file)

    if hour != time.localtime().tm_hour:
        hour = time.localtime().tm_hour
        # Get the data from the server and put them on the yaml
        with open('tmp/usage.yaml', 'r') as file:
            data = yaml.safe_load(file)
        data["ram"][hour] = round(psutil.virtual_memory()[3]/1000000000, 2) / int(round(psutil.virtual_memory()[0]/1000000000, 0)) * 100
        data["cpu"][hour] = psutil.getloadavg()[2] / os.cpu_count() * 100
        data["disk"][hour] = 100- round(psutil.disk_usage('/')[2]/1000000000, 2) / int(round(psutil.disk_usage('/')[0]/1000000000, 0)) *100
        print(data)
        with open('tmp/usage.yaml', 'w') as file:
            data = yaml.dump(data, file)


    time.sleep(60)


