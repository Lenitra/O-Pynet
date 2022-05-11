import os
import time
import psutil

import yaml



hour = -1
min = 9999

while True: 
    
    time.sleep(30)
    min = time.localtime().tm_min
    with open('tmp/drcdata.yaml', 'r') as file:
        data = yaml.safe_load(file)
    
    hour = time.localtime().tm_hour
    min = time.localtime().tm_min

    try:
        data["cpu"][f"{hour}.{min}"]
    except:
        data["ram"][f"{hour}.{min}"] = psutil.virtual_memory()[2]
        data["cpu"][f"{hour}.{min}"] = psutil.getloadavg()[2] / os.cpu_count() * 100
        data["disk"][f"{hour}.{min}"] = psutil.disk_usage('/')[3]

    if len(data["ram"]) > 60:
        data["ram"].popitem()
        data["cpu"].popitem()
        data["disk"].popitem()

    with open('tmp/drcdata.yaml', 'w') as file:
        data = yaml.dump(data, file)
