from encodings import utf_8
import os
import random
import requests
import shutil
import urllib.request

with open('insta/uncheck/page.html', 'r', encoding="utf_8") as file:
    html = file.read()
for e in html.split('"'):
    if e.startswith("https://cdn.discordapp.com/attachments/"):
        if e.endswith(".jpg") or e.endswith(".png") or e.endswith("jepg"):
            print(e)
            img = requests.get(e)
            with open("insta/uncheck/"+str(len(os.listdir('insta/uncheck/'))+1)+".jpg", 'wb') as f:
                f.write(img.content)
