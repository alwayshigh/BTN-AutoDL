import bencode
import hashlib
import time
import re
import requests
import json

from requests.auth import HTTPBasicAuth
from btnautodl.lib.logging import Logging


class Utorrent():

    def __init__(self, username, password, port):
        self.username = username
        self.password = password
        self.port = port
        self.hash = None

        #self.torrentList = self.__getTorrentList()

    def use(self, torrent):
        self.torrent = torrent
        self.metainfo = self.__torrentMetainfo(torrent)
        self.hash = hashlib.sha1(bencode.bencode(self.metainfo["info"])).hexdigest()

    def get(self):
        self.__request(params=params)

    def getName():
        info = re.match("^(.+)\.([^\.].+)$",info["info"]["name"]).group(1) + ".torrent"

    def setLabel(self, label):
        params = "&action=setprops&s=label&hash=" + self.hash + "&v=" + label + "&t=" + re.sub("\.", "", str(round(time.time(), 4)))
        self.__request(params=params)

    def getFiles(self):
        files = []
        for f in self.metainfo["info"]["files"]:
            files.append(f['path'][0])

        for t in self.torrentList:
            if t[2] in files:
                if t[1] == 201 and t[4] < 1000:
                    # start monitoring
                    print("Torrent not finished")
        return files

    def __torrentMetainfo(self, torrentFile):
        torrentFile = open(torrentFile, "rb")
        return bencode.bdecode(torrentFile.read())

    def getTorrentList(self):
        params = "&list=1&getmsg=1&cid=0&t=" + re.sub("\.", "", str(round(time.time(), 4)))
        torrentList = self.__request(params=params)
        return json.loads(torrentList.text)['torrents']

    def __request(self, params=""):
        url = "http://127.0.0.1:" + self.port + "/gui/"
        token = self.__getWebUIToken()
        if token:
            a = requests.get(
                url + "?token=" + token + params,
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
            'http://127.0.0.1:' + self.port + '/gui/token.html',
            data=data,
            auth=HTTPBasicAuth(self.username, self.password)
        )
        if a.status_code == 200:
            token = re.search(";'>(.+)<\/div>", a.text).group(1)
            return token
        else:
            print("Unable to connect to WebUI, please check your settings.")

    def __buildTorrentInfo(self, torrentInfo):
        return {
            "hash": data[0],
            "status": data[1],
            "name": data[2],
            "size": self.humansize(data[3]),
            "percentDone": str(data[4] / 10) + "%",
            "downloaded": self.humansize(data[5]),
            "uploaded": self.humansize(data[6]),
            "ratio": data[7] / 1000,
            "uploadSpeed": self.humansize(data[8]) + "/s",
            "downloadSpeed": self.humansize(data[9]) + "/s",
            "timeRemaining": str(round((data[10] / 60), 2)) + "minutes",
            "label": data[11],
            "peersConnected": data[12],
            "peersTotal": data[13],
            "seedsConnected": data[14],
            "seedsTotal": data[15],
            "unknown": data[16],
            "id": data[17],
            "remaining": data[18]
        }
