# BTN-AutoDL

- [Installation](#installation)
- [Configuartion](#configuration)
- [Filters](#filters)
- [FAQ](#faq)

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
#### *download-log*
Options: `Yes, No`  

#### *new-season-folder*
Options: `Yes, No`  

#### *authkey*
#### *passkey*
#### *torrent_dir*
#### *utorrent_dir*
#### *utorrent_label*
#### *webui_port*
#### *webui_username*
#### *webui_password*
## Filters
### Global Filters
Global Filters are used to help store repetitivly used filters to reduce repeating yourself. You then can reference them in the [local filters](#local filters) using `filter=`.

#### EXAMPLE:
```
[filter 720p HDTV Scene]
release-type = Episode
container = MKV
codec = H.264
source = HDTV
resolution = 720p
scene = Yes
```


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
Match a scene Release.  
Options: `Yes, No`  

#### *fast-torrent*
Match release marked a fast torrent (24mbit or faster)  
Options: `Yes, No`  

#### *uploader*
Match releases for certain BTN uploader.  
Example: `uploader = AlwaysHigh`    

#### *except-tags*
Filter out certain keywords in release name.  
Example: `except-tags = proper, internal`  

#### *release-group*
Match releases from certain encode groups.  
Example: `release-group = NTb`

### Local Filters

#### *filter*
Title of global filter to inherit filter from.  
Example: `filter = 720p WEB-DL, 1080p WEB-DL`

#### *save-to*
Directory where your series files will be saved. You can have a save-to for each filter used.
Example:
```
Existing Folder:
save-to = C:\Tv Series\The Walking Dead\The.Walking.Dead.S06.720p.HDTV.x264-AVS

New Folder:
save-to = C:\Tv Series\The Walking Dead\

Multiple Folders:
save-to(720p WEB-DL) = C:\Tv Series\The Walking Dead\The.Walking.Dead.S06.720p.WEB-DL.H.264-Cyphanix
save-to(720p Scene) = C:\Tv Series\The Walking Dead\The.Walking.Dead.S06.720p.HDTV.x264-AVS
```
**note:** If you dont have an existing folder for this series releases end path with a trailing slash as this will prompt the script to create a new directory based on the release name or, (Coming Soon, Custom folder format using macros)

#### *enabled*
Enabled filter to download matches.  
Options: `Yes, No`

### Frequently Asked Questions


