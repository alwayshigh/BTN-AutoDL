import pprint
import bencode
import hashlib
import os
from pathlib import Path
import re
import time
import requests
from requests.auth import HTTPBasicAuth
import json
from atomicwrites import atomic_write


class UTorrent():
    def __init__(self, username="alwayshigh", password="penis123", port="48983", ip="127.0.0.1"):
        self.username = username
        self.password = password
        self.ip = ip
        self.port = port
        self.url = "http://{}:{}".format(self.ip,self.port)

    def getTorrentList(self):
        params = "&list=1&getmsg=1&cid=0&t=" + re.sub("\.", "", str(round(time.time(), 4)))
        torrentList = self.__request(params=params)
        return json.loads(torrentList.text)['torrents']

    def __request(self, params=""):
        token = self.__getWebUIToken()
        if token:
            a = requests.get(
                self.url + "/gui/?token=" + token + params,
                headers={"content-type": "application/json"},
                auth=HTTPBasicAuth(self.username, self.password)
            )
            if a.status_code == 200:
                return a
            else:
                print("Request to WebUI failed, please check your settings.")

    def __getWebUIToken(self):
        data = {"t": re.sub("\.", "", str(round(time.time(), 4)))}
        a = requests.get(
            self.url + "/gui/token.html",
            data=data,
            auth=HTTPBasicAuth(self.username, self.password)
        )
        if a.status_code == 200:
            token = re.search(";'>(.+)<\/div>", a.text).group(1)
            return token
        else:
            print("Unable to connect to WebUI, please check your settings.")


saveToPath = "F:\American Dad!\American.Dad.S14.1080p.WEB-DL.DD5.1.H.264-ViSUM"

torrent = "C:\Users\Jesse\Downloads\American.Dad.S14.1080p.iT.WEB-DL.DD5.1.H.264-ViSUM.[BTN].torrent"
torrent = open(torrent, "rb")
metainfo = bencode.bdecode(torrent.read())
torrentHash = hashlib.sha1(bencode.bencode(metainfo["info"])).hexdigest()

failed = []

files = metainfo["info"]["files"]

season = {
    "name": metainfo["info"]["name"].rstrip("."),
    "incomplete": [],
    "missing": []
}

ut = UTorrent()
torrentList = ut.getTorrentList()
for torrentInfo in files:
    path = saveToPath + "\\" + torrentInfo["path"][0]
    torrentFile = Path(path)
    if torrentFile.exists():
        for torrent in torrentList:
            if torrent[2] == torrentInfo["path"][0]:
                if int(torrent[4]) != 1000:
                    season["incomplete"].append(torrentInfo)
    else:
        season["missing"].append(torrentInfo)


print("Total: ", len(files), "Incomplete: ", len(season["incomplete"]))

pprint.pprint(season)

# Torrent Status id's
# Stopped 136
# Downloading 201
# Force Download 137
# Paused 233
# hash checking 130