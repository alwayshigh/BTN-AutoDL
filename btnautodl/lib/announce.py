import ConfigParser
import errno
import re
import os
import subprocess

from timeit import default_timer as timer

from btnautodl.lib.logging import Logging

class AnnounceParser():

    def __init__(self, filters):
        self.config = ConfigParser.RawConfigParser()
        self.config.read(filters)
        self.logging = Logging()

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
            "episode"
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

            userFilters = self.__buildUserFilters(announceFilters)

            # cross checks users filters for matches with announce
            if self.__filterMatch(announceFilters, userFilters):
                seasonDirectory = self.data["directory"] = self.__directoryPath(announceFilters)
                self.data["success"] = self.__download(seasonDirectory, announceFilters)
            self.data["executeTime"] = round(((timer() - start)), 3)
        return self.data

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
                for i, f in enumerate(userFilters):
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
            passed = True
            for optionName, optionList in filterOptions.items():
                if optionName == "language":
                    if int(announceFilters["language"]):
                        passed = False
                        languageOptions = configparser.ConfigParser()
                        langini = hexchatDir + "/addons/resources/languages.ini"
                        languageOptions.read(langini)
                        for language in optionList:
                            if languageOptions.has_option("language", language):
                                passed = True
                                break
                elif optionName == "except-tags":
                    for tag in optionList:
                        if re.search('(?<!^)' + tag + '(?!$)', announceFilters['release-name'], re.IGNORECASE):
                            passed = False
                elif announceFilters[optionName].lower() not in optionList:
                    passed = False
            if passed:
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
        if announceFilters['episode'] == "01" or saveToDirectory.endswith("/"):
            saveToDirectory = self.__createSeasonDirectory(announceFilters, saveToOption, saveToDirectory)
        return saveToDirectory

    def __createSeasonDirectory(self, announceFilters, saveToOption, seasonPath):
        if not seasonPath.endswith("/"):
            seasonPath = seasonPath.rsplit("/", 1)[0] + "/"

        if announceFilters['scene'] == "Yes":
            seasonFolderName = re.sub(
                r"[^-]*$",
                "BTN",
                announceFilters["release-name"]
            )

        if self.config.has_option("settings", "folder_format"):
            self.logging.warning("macro-not-set")
        else:
            if announceFilters["resolution"] == "SD":
                match = r"(" + announceFilters['series'] + ".+?)(" + announceFilters["source"] + ")"
            else:
                match = r"(^.+S" + announceFilters['season'] + ").+?(" + announceFilters["resolution"] + ".*$)"

        seasonFolderName = re.match(match, announceFilters["release-name"], re.IGNORECASE).group(1, 2)
        seasonFolderName = ".".join(seasonFolderName)
        seasonFullPath = seasonPath + seasonFolderName

        self.config.set(announceFilters["title"], saveToOption, seasonFullPath)
        with open(filterini, "w") as configFile:
            self.config.write(configFile)

        try:
            os.makedirs(seasonFullPath)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

        return seasonFullPath

    def __checkSeasonFiles(self, announceFilters):
        torrent = "C:/Users/Jesse/Downloads/Fear.the.Walking.Dead.S02.720p.WEB-DL.DD5.1.H.264-NTb.[BTN].torrent"
        torrentFile = open(torrent, "rb")
        info = bencode.bdecode(torrentFile.read())

        seasonFilenames = []
        for index in range(len(info['info']['files'])):
            seasonFilenames.extend(info['info']['files'][index]["path"])

        torrentList = self.getTorrentList()
        torrentList = json.loads(torrentList.text)['torrents']
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
        if files:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute('''INSERT INTO monitor VALUES ({},{},{},{},{})''').format(
                announcerFilters["name"],
                files,
                hashId,
                save_dir,
                torrentFile
            )

    def __download(self, seasonDirectory, announceFilters):
        settings = {}
        for d in self.config.options("settings"):
            settings[d] = self.config.get("settings", d).replace("\\", "/")

        url = "https://broadcasthe.net/torrents.php?action=download&id="
        torrentUrl = url + announceFilters["id"] + "&authkey=" + settings['authkey'] + "&torrent_pass=" + settings['passkey']
        torrentFile = settings['torrent_dir'] + "/" + announceFilters["release-name"] + ".torrent"

        torrentContent = requests.get(torrentUrl)
        with open(torrentFile, "wb") as torrent:
            torrent.write(torrentContent.content)

        if announceFilters["release-type"] == "Season":
            if not self.__checkSeasonFiles(announceFilters, seasonDirectory, torrentFile):
                return False

        subprocess.call("\"" + settings['utorrent_dir'] + "/utorrent.exe\"" + " /MINIMIZED /DIRECTORY \"" + seasonDirectory + "\" \"" + torrentFile + "\"",stderr=subprocess.STDOUT)
        print(stderr)
        try:
            label = settings["utorrent_label"]
            webui = Utorrent(settings["webui_username"], settings["webui_password"], settings["webui_port"])
            webui.use(torrentFile)
            webui.setLabel(label)
        except KeyError:
            pass
        return True