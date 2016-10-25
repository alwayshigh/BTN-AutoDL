messages = {
    "download": "\002{d[0]}\017 - {d[1]}\017\n" \
                "{d[2]} - {d[3]} - {d[4]} - {d[5]}  |  Time: {d[6]} seconds\n" \
                "{d[7]}",
    "global-filter-not-used": "{d[0]} is not using global filters. We advise to use over local filters",
    "global-filter-not-set": "Global filter doesnt exist: {d[0]}",
    "save-to-not-set": "{d[0]} has no 'save-to' filter option.",
    "save-to-default": "Saving to clients default download folder.",
    "macro-not-set": "Marcros are not set up.",
    "unexpected-error": "Something went wrong \n"
                        "and we dont know what.",
    "help": "Command List:\n"
            "Usage: /autodl [OPTIONS] [COMMAND] [ARGS]\n"
            "# Downloads torrent if filters match. Copy announce from #BTN-WhatAuto, use quotations.\n"
            "DOWNLOAD <announce_string>\n"
            "# Adds new filters/series. Use | to split filter options.\n"
            "ADD filter|series <name> filters=<filtername>:<val>,<val>\n"
            "# Delete selected filter/series.\n"
           r"DELETE filters|series <name>\n"
            "# List active downloads from uTorrent.\n"
            "TORRENT list\n"
            "# Print torrent stats to current channel.\n"
            "TORRENT view <torrent_name>\n"
            "# Display this help ouput\n"
            "HELP"
}
