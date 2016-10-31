# BTN-AutoDL

- [Installation](#installation)
- [Configuartion](#configuration)
- [Filters](#filters)

## Installation
1. **Download HexChat v2.12.3**  
  Windows 7/8/10: ( [x86](https://dl.hexchat.net/hexchat/HexChat%202.12.3%20x86.exe) / [x64](https://dl.hexchat.net/hexchat/HexChat%202.12.3%20x64.exe) )
  
2. **Install HexChat**  
  When Installing HexChat please select the options below. If you already have HexChat installed rerun the the installer to install python capabilities. None of your current settings will be changed.
  
  ![alt text](http://oi63.tinypic.com/2rna7bo.jpg "Hexchat Python install")
  
3. **Install Python Modules**  
  Run Command Prompt as administrator and enter the following:  
  ```
pip install bencode ConfigParser errno timeit hashlib
  ```  
  If you fail to find pip use the below code instead.  
  ```
C:\Python27\Scripts\pip.exe install bencode ConfigParser errno timeit hashlib
  ```  
  
  
4. **BTN AutoDL**
  - Download BTN AutoDL.
  - ![alt text](http://i66.tinypic.com/331dqir_th.png "Windows Key") ![alt text](http://i65.tinypic.com/eg8m0n_th.png "Plus") ![alt text](http://icons.iconarchive.com/icons/chromatix/keyboard-keys/32/letter-uppercase-R-icon.png "R Key") enter `%appdata%/hexchat/addons`
  - Copy `btnautodl.py` and `btnautodl` to the directory above. 
  
## Configuration
#### download-log
Option: `Yes, No`  
#### new-season-folder
Option: `Yes, No`  
#### authkey
#### passkey
#### torrent_dir
#### utorrent_dir
#### utorrent_label
#### webui_port  
#### webui_username
#### webui_password
## Filters
### Global Filters
#### release-type
Description: Matches release type.  
Options: `Season, Episode`  
#### year
Description: Match year of show release.  
Example: `year = 2015,2016`  
#### season
Description: Match exact season number.  
Example: `season = 6`  
#### episode
Description: Match exact season number.  
Example: `episode = 13` 
#### container
Options: `AVI, MKV, VOB, MPEG, MP4, ISO, WMV, TS, M4V, M2TS`  
#### codec
Options: `XViD, x264, MPEG2, DiVX, DVDR, VC-1, h.264, WMV, BD, x264-Hi10P`  
#### source
Options:  `HDTV, PDTV, DSR, DVDRip, TVRip, VHSRip, Bluray, BDRip, BRRip, DVD5, DVD9, HDDVD, WEB-DL, WEBRip BD5, BD9, BD25, BD50, Mixed, Unknown`  
#### resolution
Options: `SD, 720p, 1080p, 1080i, Portable Device`
#### scene
Description: Match a scene Release.  
Options: `Yes, No`  
#### fast-torrent
Description: Match release marked a fast torrent (24mbit or faster)  
Options: `Yes, No`  
#### uploader
Description: Match releases for certain BTN uploader.  
Example: `uploader = AlwaysHigh`    
#### except-tags
Description: Filter out certain keywords in release name.  
example: `except-tags = proper, internal`  
#### release-group
Description: Match releases from certain encode groups.  
Exampe: `release-group = NTb`

### Local Filters
#### filter
Description: Title of global filter to inherit filter from.  
Option: `string`  
#### save-to
Description: Directory where your series files will be saved.
Option: `string`  
#### enabled
Description: Enabled filter to download matches
Option: `Yes, No`

