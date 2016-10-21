import bencode
import hashlib
import time
import re
import requests
from requests.auth import HTTPBasicAuth

from btnautodl.lib.logging import Logging

class Utorrent():

    def __init__(self, username, password, port):
        self.username = username
        self.password = password
        self.port = port
        self.hash = None       

    def use(self, torrent):
        self.hash = self.__getTorrentHash(torrent)

    def get(self):
        headers = {"content-type": "application/json"}
        params = "&list=1&getmsg=1&cid=0&t=" + re.sub("\.", "", str(round(time.time(), 4)))
        torrentList = self.__request(params=params, headers=headers)
        if torrentList:
            torrentList = json.loads(torrentList.text)['torrents']
            torrents = {}
            for t in torrentList:
                if t[1] == 201 and t[4] < 1000:
                    torrents = self.__buildTorrentInfo(t)
        return

    def setLabel(self, label):
        headers = {"content-type": "application/json"}
        params = "&action=setprops&s=label&hash=" + self.hash + "&v=" + label + "&t=" + re.sub("\.", "", str(round(time.time(), 4)))
        self.__request(params=params, headers=headers)

    def __getTorrentHash(self, torrent):
        torrentFile = open(torrent, "rb")
        metainfo = bencode.bdecode(torrentFile.read())
        return hashlib.sha1(bencode.bencode(metainfo["info"])).hexdigest()

    def __getToken(self):
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

    def __request(self, params="", headers={}):
        url = "http://127.0.0.1:" + self.port + "/gui/"
        token = self.__getToken()
        if token:
            a = requests.get(
                url + "?token=" + token + params,
                headers=headers,
                auth=HTTPBasicAuth(self.username, self.password)
            )
            if a.status_code == 200:
                return a
            else:
                print("Request to WebUI failed, please check your settings.")

    def __buildTorrentInfo(self, data):
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