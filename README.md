# BTN-AutoDL

- [Installation](#installation)
- [Configuartion](#configuration)
- [Filters](#filters)
  * [Global Filters](#global-filters)
  * [Local Filters](#local-filters)
- [FAQ](#frequently-asked-questions)

## Overview
BTN AutoDL was built automate the downloading of shows in an organised manner. It allows you to specify filters to match your required release and store your downloads in tidy directory format you choose depending on ur settings. No more moving files around. It was **not** created in order to peform wildcard matches like irssi-autodl for you upload whores ie.`match-releases = *`

## Installation
1. **HexChat v2.12.3**  

  ![alt text](http://oi63.tinypic.com/2rna7bo.jpg "Hexchat Python install")  
  **Important:** You will need to rerun hexchat installer to enabled Python 2.7 plugin support. If you already have HexChat, reinstalling wont edit your current HexChat settings.  
  
2. **Python Modules**  
  Run Command Prompt as administrator and enter the following:  
  ```
pip install bencode ConfigParser errno timeit hashlib
  ```  
  If you fail to find pip use the below code instead.  
  ```
C:\Python27\Scripts\pip.exe install bencode ConfigParser errno timeit hashlib
  ```  

3. **uTorrent Web UI**  
  Some functions of this script require access to uTorrents optional Web UI.  
  
  To install follow this small tutorial - [Web UI Tutorial](http://www.htpcguides.com/setup-utorrent-remote-access-webui/)  
  
  Remember the username/password/port you used as they will be needed for BTN AutoDL configuration. For the purposes of this script I recommend limiting Web UI access to localhost IP: `127.0.0.1`  
  
  **Note:** You can use an alternative Web UI port or uTorrents listening port set in `Options->Prefrences->Connection`
  
4. **BTN AutoDL**  
  Download BTN AutoDL.  
  ![alt text](http://i66.tinypic.com/331dqir_th.png "Windows Key") ![alt text](http://i65.tinypic.com/eg8m0n_th.png "Plus") ![alt text](http://icons.iconarchive.com/icons/chromatix/keyboard-keys/32/letter-uppercase-R-icon.png "R Key") enter `%appdata%/hexchat/addons`  
  Copy `btnautodl.py` and `btnautodl` to the directory above.  
  
## Configuration
#### *download-log*
Enable logging of new matched downloads in a HexChat log tab.  
Options: `Yes, No`  
#### *authkey*
Personal BTN authkey  
[How to get passkey?](#frequently-asked-questions)
#### *passkey*
Personal BTN passkey  
[How to get passkey?](#frequently-asked-questions)
#### *torrent-dir*
Directory to save all .torrent files  
#### *utorrent-dir*
Directory path to the utorrent.exe  
#### *utorrent-label*
Set a uTorrent label for all downloads.  
#### *webui-port*
Port set when instaling utorent Web UI.  
#### *webui-username*
Username set when instaling utorent Web UI.  
#### *webui-password*
Password set when instaling utorent Web UI.  

## Filters
Global Filters are used to help store repetitivly used filters to reduce repeating yourself. You then can reference them in the Local Filters using [`filter=`](#local-filters). Below is a basic example to download The Walking Dead as 720p HDTV Scene release.

Example:
```
[filter 720p HDTV Scene]
release-type = Episode
container = MKV
codec = H.264
source = HDTV
resolution = 720p
scene = Yes

[The Walking Dead]
filter = 720p HDTV Scene
save-to = C:\Tv Series\The Walking Dead\The.Walking.Dead.S06.720p.HDTV.x264-AVS
```
### Global Filters

#### *release-type*
Matches release type.  
Options: `Season, Episode`  

#### *year*
Match year of show release.  
Example: `year = 2015,2016`  

#### *season*
Match exact season number.  
Example: `season = 6`  

#### *episode*
Match exact season number.  
Example: `episode = 13` 

#### *container*
Options: `AVI, MKV, VOB, MPEG, MP4, ISO, WMV, TS, M4V, M2TS`  

#### *codec*
Options: `XViD, x264, MPEG2, DiVX, DVDR, VC-1, h.264, WMV, BD, x264-Hi10P`  

#### *source*
Options:  `HDTV, PDTV, DSR, DVDRip, TVRip, VHSRip, Bluray, BDRip, BRRip, DVD5, DVD9, HDDVD, WEB-DL, WEBRip BD5, BD9, BD25, BD50, Mixed, Unknown`

#### *resolution*
Options: `SD, 720p, 1080p, 1080i, Portable Device`

#### *scene*
Matches scene Release.  
Options: `Yes, No`  

#### *fast-torrent*
Matches release marked a fast torrent (24mbit or faster)  
Options: `Yes, No`  

#### *uploader*
Matches releases for certain BTN uploader.  
Example: `uploader = AlwaysHigh`    

#### *except-tags*
Wont download releases with certain keywords in release name.  
Example: `except-tags = proper, internal`  

#### *release-group*
Matches release from certain encode groups.  
Example: `release-group = NTb`

### Local Filters

#### *filter*
Name of global filter to inherit filters from.  
Example: `filter = 720p WEB-DL, 1080p WEB-DL`

#### *save-to*
Directory where your release files will be saved. You can have a save-to for each filter used.
Example:
```
Existing Folder:
save-to = C:\Tv Series\The Walking Dead\The.Walking.Dead.S06.720p.HDTV.x264-AVS

New Folder:
save-to = C:\Tv Series\The Walking Dead\

Multiple Folders:
save-to(720p WEB-DL) = C:\Tv Series\The Walking Dead\The.Walking.Dead.S06.720p.WEB-DL.H.264-Cyphanix
save-to(720p HDTV Scene) = C:\Tv Series\The Walking Dead\The.Walking.Dead.S06.720p.HDTV.x264-AVS
```
**note:** If you dont have an existing folder for this series releases end path with a trailing slash as this will prompt the script to create a new directory based on the release name or, (Coming Soon, Custom folder format using macros)

#### *enabled*
Enable filter to download matches.  
Options: `Yes, No`

### Frequently Asked Questions

1. **Where can i find my authkey or passkey?**  
Go to BTN website and right-click a torrent download button and click `copy link address` paste the contents to display your authkey and passkey like the url below copy the relevant info into your config:  
`https://broadcasthe.net/torrents.php?action=download&id=1337&authkey=a1b2c3d4e5f6g7h8i9j1k2l3m&torrent_pass=a1b2c3d4e5f6g7h8i9j1k2l3m`
