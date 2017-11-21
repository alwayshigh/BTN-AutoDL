import ConfigParser
import errno
import re
import os
import subprocess
import requests
import bencode

from timeit import default_timer as timer

from btnautodl.lib.logging import Logging
from btnautodl.lib.utorrent import Utorrent

class AnnounceParser():

    def __init__(self, filters):
        self.filters = filters
        self.config = ConfigParser.RawConfigParser()
        self.config.read(filters)
        self.logging = Logging()

        self.settings = {}
        for d in self.config.options("settings"):
            self.settings[d] = self.config.get("settings", d).replace("\\", "/")

        self.options = [
            "title",
            "series",
            "release-type",
            "year",
            "container",
            "codec",
            "source",
            "resolution",
            "scene",
            "fast-torrent",
            "id",
            "uploader",
            "language",
            "release-name",
            "release-group",
            "except-tags",
            "season",
            "episode",
            "web-source"
        ]

    def parse(self, announce):
        start = timer()
        self.data = {
            "success": False,
            "executeTime": 0
        }

        announceFilters = self.__buildAnnounceFilters(announce)
        self.data["options"] = announceFilters

        # Check if series in filter list and not disabled
        if self.config.has_section(announceFilters["title"]):
            if self.config.has_option(announceFilters["title"], "enabled"):
                if self.config.get(announceFilters["title"], 'enabled').lower() == "no":
                    self.data["success"] = False
                    return self.data
            userFilters = self.__buildUserFilters(announceFilters)
            # cross checks users filters for matches with announce
            if self.__filterMatch(announceFilters, userFilters):
                saveToPath = self.data["directory"] = self.__directoryPath(announceFilters)
                try:
                    torrentFile = self.settings["torrent-dir"] + "/" + announceFilters["release-name"] + ".[BTN].torrent"
                    self.__getTorrent(torrentFile, announceFilters["id"])

                    if announceFilters["release-type"] == "Season":
                        if not self.__checkSeasonFiles(announceFilters, saveToPath, torrentFile):
                            self.data["success"] = False
                    else:
                        self.data["success"] = self.__download(saveToPath, torrentFile)
                except (IndexError, KeyError) as e:
                    self.logging.error(msgId="torrent-dir")
                    self.data["success"] = False

            self.data["executeTime"] = str(round(((timer() - start)), 3))
        return self.data

    def download(self, downloadUrl):
        torrentFilePath = self.settings["torrent-dir"]
        torrentFile = torrentFilePath + "/btnautodl_manual_download.torrent"
        self.__getTorrent(torrentFile, url=downloadUrl)

    def __getTorrent(self, torrentFile, torrentId):
        url = "https://broadcasthe.net/torrents.php?action=download&" + \
              "id=" + torrentId + "&authkey=" + self.settings['authkey'] + "&torrent_pass=" + self.settings['passkey']        
        
        torrentContent = requests.get(url)
        with open(torrentFile, "wb") as torrent:
            torrent.write(torrentContent.content)

    def __download(self, saveToPath, torrentFile):
        try:
            subprocess.call("\"" + self.settings['utorrent-dir'] + "/utorrent.exe\"" + " /MINIMIZED /DIRECTORY \"" + saveToPath + "\" \"" + torrentFile + "\"")
        except IndexError:
            self.logging.error("config_no_utorrent")
            return False

        try:
            label = self.settings["utorrent-label"]
            utorrent = Utorrent(self.settings["webui-username"], self.settings["webui-password"], self.settings["webui-port"])
            utorrent.use(torrentFile)
            utorrent.setLabel(label)
        except KeyError, IndexError:
            pass
        return True

    def __buildAnnounceFilters(self, announce):
        filters = {}
        announce = announce.split(" | ")
        for i, value in enumerate(announce):
            try:
                filters[self.options[i]] = str(announce[i].strip(" "))
            except AttributeError:
                continue
        try:
            filters["season"], filters["episode"] = re.match("S(\d+)E(\d+)", filters["series"]).group(1, 2)
        except AttributeError:
            try:
                filters["season"] = re.match("Season\s(\d+)$", filters["series"]).group(1)
            except AttributeError:
                filters["season"] = filters["year"]

        if filters["language"] != "English":
            filters["language"] = re.match(".+(\d+)$", filters["language"]).group(1)
        try:
            filters["release-group"] = re.match(".+-([^-].+)$", filters["release-name"]).group(1)
        except AttributeError:
            filters["release-group"] = ""
        return filters

    def __buildUserFilters(self, announceFilters):
        """
        Parse Global/Local Series Filters to form a dictionary
        filters["filter WEB 720p"]["Source"]["WEBRip","WEB-DL"]
        """
        userFilters = {}
        if self.config.has_option(announceFilters["title"], "filter"):
            filters = self.config.get(announceFilters["title"], "filter").split(",")
            # Loop through global filters set for series
            for f in filters:
                f = "filter " + f.strip(" ")
                if self.config.has_section(f):
                    userFilters = self.__getFilterOptions(f, userFilters, False)
                else:
                    return logging.error("no-global-filter", msgData=[f])
        else:
            logging.warning("global-filter-not-used", msgData=[announceFilters["title"]])
        userFilters = self.__getFilterOptions(announceFilters["title"], userFilters, True)
        return userFilters

    def __getFilterOptions(self, filterName, userFilters, isLocal=False, aliasName=None):
        if isLocal:
            if len(userFilters) > 0:
                for f in userFilters:
                    userFilters = self.__getFilterOptions(filterName, userFilters, False, f)
            else:
                userFilters = self.__getFilterOptions(filterName, userFilters, False)
            return userFilters

        if not aliasName:
            aliasName = filterName

        if aliasName not in userFilters:
            userFilters[aliasName] = {}

        for option in self.options:
            if self.config.has_option(filterName, option):
                filters = self.config.get(filterName, option).split(",")
                if filters:
                    if option not in userFilters[aliasName]:
                        userFilters[aliasName][option] = []
                    for f in filters:
                        f = f.strip(" ")
                        if f.lower() not in userFilters[aliasName][option]:
                            userFilters[aliasName][option].append(f.lower())
        return userFilters

    def __filterMatch(self, announceFilters, userFilters):
        
        for filterName, filterOptions in userFilters.items():
            filterPassed = True
            for optionName, optionList in filterOptions.items():
                optionPassed = True
                if optionName == "language":
                    if int(announceFilters["language"]):
                        optionPassed = False
                        languageOptions = configparser.ConfigParser()
                        langini = hexchatDir + "/addons/resources/languages.ini"
                        languageOptions.read(langini)
                        for language in optionList:
                            if languageOptions.has_option("language", language):
                                optionPassed = True
                                break
                elif optionName == "except-tags":
                    for tag in optionList:
                        if re.search('(?<!^)' + tag + '(?!$)', announceFilters['release-name'], re.IGNORECASE):
                            optionPassed = False
                elif optionName == "web-source":
                    if announceFilters["source"] in ["WEB-DL", "WEBRip"]:
                        webSourceAliases = {
                            "itunes": ["itunes", "it"],
                            "amazon": ["amazon", "amzn"],
                            "netflix": ["netflix", "nf"],
                            "tvland": ["tvland", "tvl"],
                            "hulu": ["hulu"],
                            "epix": ["epix"]
                        }
                        for webSource in optionList:
                            optionPassed = False
                            if webSource in webSourceAliases:
                                aliases = "|".join(webSourceAliases[webSource])
                                regex = "(?<!^){}[\.|\s]{}(?!$)".format(aliases, announceFilters["source"])
                                result = re.findall(regex, announceFilters['release-name'], re.IGNORECASE)
                                if result:
                                    optionPassed = True
                                    break
                elif announceFilters[optionName].lower() not in optionList:
                    optionPassed = False

                if not optionPassed:
                    filterPassed = optionPassed
                    break
            if filterPassed:
                self.globalFilter = filterName
                return True
        return False

    def __directoryPath(self, announceFilters):
        try:
            saveToOption = "save-to(" + re.sub("filter ", "", self.globalFilter) + ")"
            saveToDirectory = self.config.get(announceFilters["title"], saveToOption).replace('\\', '/')
        except ConfigParser.NoOptionError:
            try:
                saveToOption = "save-to"
                saveToDirectory = self.config.get(announceFilters["title"], saveToOption).replace('\\', '/')
            except ConfigParser.NoOptionError:
                self.logging.warning("save-to-not-set", msgData=[announceFilters["title"]])
                self.logging.info("save-to-default")
                return None
        if 'episode' in announceFilters:
            if announceFilters['episode'] == "01" or saveToDirectory.endswith("/"):
                saveToDirectory = self.__createSeasonDirectory(announceFilters, saveToOption, saveToDirectory)
        return saveToDirectory

    def __createSeasonDirectory(self, announceFilters, saveToOption, seasonPath):
        if not seasonPath.endswith("/"):
            seasonPath = seasonPath.rsplit("/", 1)[0] + "/"

        try:
            folderFormat = self.settings["folder-format"]
            self.logging.warning("macro-not-set")
        except KeyError:
            pass

        if announceFilters['scene'] == "Yes":
            announceFilters['release-group'] = "BTN"

        if announceFilters["codec"] == "H.264":
            if re.search("(x264)", announceFilters["release-name"], re.IGNORECASE):
                codec = "x264"
            else:
                codec = announceFilters["codec"]

        m = r"(^.+?)[\.|\s]{}".format(announceFilters["series"], announceFilters["source"])
        season = re.match(m, announceFilters["release-name"], re.IGNORECASE).group(1).replace(" ", ".")

        if announceFilters["resolution"] == "SD":
            folderName = "{}.S{}.{}.{}-{}".format(
                season,
                announceFilters["season"],
                announceFilters["source"],
                codec,
                announceFilters["release-group"]
            )
        else:
            folderName = "{}.S{}.{}.{}.{}-{}".format(
                season,
                announceFilters["season"],
                announceFilters["resolution"],
                announceFilters["source"],
                codec,
                announceFilters["release-group"]
            )
            
        seasonFullPath = seasonPath + folderName
        self.config.set(announceFilters["title"], saveToOption, seasonFullPath)
        with open(self.filters, "w") as configFile:
            self.config.write(configFile)

        try:
            os.makedirs(seasonFullPath)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

        return seasonFullPath

    def __checkSeasonFiles(self, announceFilters, saveToPath, torrentFile):
        # torrentFile = open(torrentFile, "rb")
        # info = bencode.bdecode(torrentFile.read())

        # seasonFilenames = []
        # for index in range(len(info['info']['files'])):
        #     seasonFilenames.extend(info['info']['files'][index]["path"])

        utorrent = Utorrent(self.settings["webui-username"], self.settings["webui-password"], self.settings["webui-port"])
        utorrent.use(torrentFile)
        torrentList = utorrent.torrentList()
        torrentFilenames = []
        torrentFileDetails = []
        for torrent in torrentList:
            torrentFilenames.append(torrent[2])
            torrentFileDetails.append({
                "completed": torrent[4],
                "status": torrent[1]
                })

        files = []
        for filename in seasonFilenames:
            if filename in torrentFilenames:
                i = torrentFilenames.index(filename)
                if int(torrentFileDetails[i]["completed"]) < 1000 and int(torrentFileDetails[i]["status"]) == 136:
                    files.append(filename)

        files = ",".join(files)
        self.logging.log(files)       
        # if files:
        #     conn = sqlite3.connect("database.db")
        #     c = conn.cursor()
        #     c.execute('''INSERT INTO monitor VALUES ({},{},{},{},{})''').format(
        #         announcerFilters["name"],
        #         files,
        #         hashId,
        #         save_dir,
        #         torrentFile
        #     )

# filterini = "C:\\Users\\Jesse\\AppData\\Roaming\\HexChat\\addons\\btnautodl\\btnautodl\\filters.ini"
# announceFilters = "American Dad! | Season 14 | Season | 2017 | MKV | H.264 | WEB-DL | 1080p | No | Yes | 831974 | truedread | English | American.Dad.S14.1080p.iT.WEB-DL.DD5.1.H.264-ViSUM"
# torrentFile = "C:\\Users\\Jesse\\Downloads\\American.Dad.S14.1080p.iT.WEB-DL.DD5.1.H.264-ViSUM.[BTN].torrent"

# btn = AnnounceParser(filterini)
# btn.parse(announceFilters)

# import pprint
# import bencode
# import hashlib
# import os
# from pathlib import Path


# saveToPath = "F:\American Dad!\American.Dad.S14.1080p.WEB-DL.DD5.1.H.264-ViSUM"

# torrent = "C:\Users\Jesse\Downloads\American.Dad.S14.1080p.iT.WEB-DL.DD5.1.H.264-ViSUM.[BTN].torrent"
# torrent = open(torrent, "rb")
# metainfo = bencode.bdecode(torrent.read())
# torrentHash = hashlib.sha1(bencode.bencode(metainfo["info"])).hexdigest()

# failed = []

# for torrentInfo in metainfo["info"]["files"]:
#     path = saveToPath + "\\" + torrentInfo["path"][0]
#     torrentFile = Path(path)
#     if torrentFile.exists():
#         stats = os.stat(path)
#         if stats.st_size != torrentInfo["length"]:
#             failed.append(torrentInfo)

# print(failed)

# # for t in torrentList:
#     # if 

