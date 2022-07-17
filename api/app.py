import os
import json
import random
import requests

from base64 import b64encode
from dotenv import load_dotenv, find_dotenv
from flask import Flask, Response, jsonify, render_template

load_dotenv(find_dotenv())


SPOTIFY_CLIENT_ID = "c3ee27eeae4342cebc6678e80b46755b"
SPOTIFY_SECRET_ID = "41024ca087064a4d8afc34dba875361b"
SPOTIFY_REFRESH_TOKEN = "AQCfqSDEOgUCADkA9THvY51oSJFyDrz2djd2lOgPHCBZj50BoT1vB4voqqUj0ODZoAs9Ds9opX1dcOkaR5IHtvSM2Jlxj1GDoTolzHHL5ALDlDAGYtwChozZnunRcrqLg6Y"


REFRESH_TOKEN_URL = "https://accounts.spotify.com/api/token"
NOW_PLAYING_URL = "https://api.spotify.com/v1/me/player/currently-playing"
RECENTLY_PLAYING_URL = (
    "https://api.spotify.com/v1/me/player/recently-played?limit=10"
)

app = Flask(__name__)


def getAuth():
    return b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_SECRET_ID}".encode()).decode(
        "ascii"
    )


def refreshToken():
    data = {
        "grant_type": "refresh_token",
        "refresh_token": SPOTIFY_REFRESH_TOKEN,
    }

    headers = {"Authorization": "Basic {}".format(getAuth())}
    response = requests.post(REFRESH_TOKEN_URL, data=data, headers=headers)

    try:
        return response.json()["access_token"]
    except KeyError:
        print(json.dumps(response.json()))
        print("\n---\n")
        raise KeyError(str(response.json()))


def recentlyPlayed():
    token = refreshToken()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(RECENTLY_PLAYING_URL, headers=headers)

    if response.status_code == 204:
        return {}
    return response.json()


def nowPlaying():
    token = refreshToken()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(NOW_PLAYING_URL, headers=headers)

    if response.status_code == 204:
        return {}
    return response.json()


def barGen(barCount):
    barCSS = ""
    left = 1
    for i in range(1, barCount + 1):
        anim = random.randint(1000, 1350)
        barCSS += (
            ".bar:nth-child({})  {{ left: {}px; animation-duration: {}ms; }}".format(
                i, left, anim
            )
        )
        left += 4
    return barCSS


def loadImageB64(url):
    resposne = requests.get(url)
    return b64encode(resposne.content).decode("ascii")


def makeSVG(data):
    barCount = 84
    contentBar = "".join(["<div class='bar'></div>" for i in range(barCount)])
    barCSS = barGen(barCount)

    if data == {} or data["item"] == "None" or data["item"] is None:
        # contentBar = "" #Shows/Hides the EQ bar if no song is currently playing
        currentStatus = "Offline"
        recentPlays = recentlyPlayed()
        recentPlaysLength = len(recentPlays["items"])
        itemIndex = random.randint(0, recentPlaysLength - 1)
        item = recentPlays["items"][itemIndex]["track"]
    else:
        item = data["item"]
        currentStatus = "Online"
    image = loadImageB64(item["album"]["images"][1]["url"])
    artistName = item["artists"][0]["name"].replace("&", "&amp;")
    songName = item["name"].replace("&", "&amp;")

    dataDict = {
        "artistName": artistName,
        "songName": songName,
        "status": currentStatus
    }

    return (dataDict)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    data = nowPlaying()
    myData = makeSVG(data)

    response = jsonify(message=myData)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    app.run(debug=True)
