import hexchat

from btnautodl.lib.messages import messages

class Logging():
    def __init__(self):
        self.__getLogTab()

    def info(self, msgId=None, msgData=None):
        if not msgId: return
        msg = "\002\00302[INFO]\017 " + self.__getLogMessage(msgId, msgData)
        self.__printToLog(msg)

    def warning(self, msgId=None, msgData=None):
        if not msgId: return
        msg = "\002\00307[WARNING]\017 " + self.__getLogMessage(msgId, msgData)
        self.__printToLog(msg)

    def error(self, msgId=None, msgData=None):
        if not msgId: return
        msg = "\002\00304[ERROR]\017 " + self.__getLogMessage(msgId, msgData)
        self.__printToLog(msg)

    def download(self, msgId=None, msgData=None):
        if not msgId: return
        msg = "\002\00309[NEW DOWNLOAD]\017 " + self.__getLogMessage(msgId, msgData)
        self.__printToLog(msg)

    def log(self, msgId=None, msgData=None):
        if not msgId: return
        msg = self.__getLogMessage(msgId, msgData)
        print(msg)

    def __getLogTab(self):
        logTabName = "BTN-AutoDL"
        if not hexchat.find_context(server=logTabName, channel=logTabName):
            loggingTab = hexchat.get_prefs('gui_tab_newtofront')
            hexchat.command('set -quiet gui_tab_newtofront 0')
            hexchat.command('newserver -noconnect {0}'.format(logTabName))
            hexchat.command('set -quiet gui_tab_newtofront {}'.format(loggingTab))
            output = """BTN AutoDL"""
            self.__printToLog(output)
        else:
            return hexchat.find_context(server=logTabName, channel=logTabName)

    def __getLogMessage(self, index, data):
        if not data:
            return messages[index]
        return messages[index].format(d=data)

    def __printToLog(self, message):
        log = self.__getLogTab()
        log.prnt(message)
        log.command('gui color 3')
