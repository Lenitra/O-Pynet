import os
import shutil
from flask import Flask, render_template, request, redirect, session
from instabot import Bot
from main import app


@app.route('/insta')
def insta():
    return render_template("insta.html")


@app.route('/post')
def post():
    try:
        shutil.rmtree("config")

    except:
        pass

    bot = Bot()

    print("")
    print("")
    print("Login en cours")
    print("")
    bot.login(username="0642760857",
              password="541!Leitmotiv")
    print("")
    print("")
    print("")
    print("Login OK")
    print("")
    print("")

    print("Upload de la photo en cours")
    print("")
    print("")
    bot.upload_photo(f"Imgs/{os.listdir('Imgs')[0]}",
                     caption="Heyyy subcribe to @waifus_hub_ to not miss anything and join us on discord (link in bio)\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nHastags\n #anime #japan #meme #art #instapics #kawaii #animewaifu #waifugirls #sexy #sexypose #waifumaterial #cosplay #cosplaysexy #animefan #animegirlkawaii #animegirl #instamoment #fun #otaku #memesdaily #meme #daily #memeaccount #manga #mangakawaii #animekawai #hentai #spicyhentaimemes")

    os.remove(f"Imgs/{os.listdir('Imgs')[0]}")
    print('Suppression')

    print('')
    print('')
    print('Terminé')
    redirect("/insta")
