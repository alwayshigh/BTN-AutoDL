__module_name__ = "BTN AutoDL"
__module_version__ = "2.0"
__module_description__ = "Download torrents that match your filters"

import hexchat
import sys
import ConfigParser
import json

pluginDirectory = hexchat.get_info('configdir') + "\\addons"
sys.path.append(pluginDirectory)

from btnautodl.lib.logging import Logging
from btnautodl.lib.announce import AnnounceParser
from btnautodl.lib.utorrent import Utorrent

logging = Logging()

filters = pluginDirectory + "btnautodl\\filters.ini"

def monitor(word, word_eol, userdata):
    if hexchat.get_info('channel') == "#BTN-WhatAuto":
        announceParser = AnnounceParser(filters)
        data = announceParser.parse(word[1])

        if data["success"]:
            location = re.sub(
                "\s",
                "%20",
                "file:///" + data["directory"] + "/" + data["options"]["release-name"] + "." + data["options"]["container"]
            )  

            logging.download("download", msgData=[
                data["options"]["title"],
                data["options"]["resolution"],
                data["options"]["source"],
                data["options"]["codec"],
                data["options"]["container"],
                data["executeTime"],
                location
            ])
       
def commands(word, word_eol, userdata):
    try:
        cmd = word[1]
        if cmd == "download":
            announceParser = AnnounceParser(filters)
            data = announceParser.parse(word[2])

            if data["success"]:
                location = re.sub(
                    "\s",
                    "%20",
                    "file:///" + data["directory"] + "/" + data["options"]["release-name"] + "." + data["options"]["container"]
                )
                logging.download("download", msgData=[
                    data["options"]["title"],
                    data["options"]["resolution"],
                    data["options"]["source"],
                    data["options"]["codec"],
                    data["options"]["container"],
                    data["executeTime"],
                    location
                ])
            else:
                logging.info("unexpected-error")
            return hexchat.EAT_ALL
        elif cmd == "display":
            config = ConfigParser.RawConfigParser()
            config.read(filters)

            option = word[2]
            section = config.sections()
            print(section)
            if option == "shows":
                output = "\00316List of Shows:\n"
                count = 0
                for section in sorted(section):
                    if not section.startswith("filter "):
                        if section != "settings":
                            output = output + section + "\n"
                            count += 1
                output = output + "Total Shows: " + str(count)
            elif option == "filters":
                output = "\00316List of Filters:\n"
                for section in sorted(section):
                    if section.startswith("filter "):
                        output = output + section + "\n"
            print(output)
        elif cmd == "season":
            utorrent = Utorrent(config)
            utorrent.checkSeasonFiles()
        elif cmd == "help":
            logging.log("help")
        return hexchat.EAT_ALL
    except IndexError:
        logging.log("help")
    return hexchat.EAT_ALL

hexchat.hook_command("AUTODL", commands)

hexchat.hook_print("Channel Message", monitor)
