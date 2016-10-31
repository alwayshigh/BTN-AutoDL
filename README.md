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
#### authkey</dt>
#### passkey</dt>
#### torrent_dir</dt>
#### utorrent_dir</dt>
#### utorrent_label</dt>
#### webui_port</dt>
#### webui_username</dt>
#### webui_password</dt>
## Filters
### Global Filters
<dl>
<dt>release-type</dt>
<dd>
Description: Matches release type.  
Options: `Season, Episode`  
</dd></dl>
<dl>
<dt>year</dt>
Description: Match year of show release.  
Example: `year = 2015,2016`  
</dd></dl>
<dl>
<dt>season</dt>
<dd>
Description: Match exact season number.  
Example: `season = 6`  
</dd></dl>
<dl>
<dt>episode</dt>
<dd>
Description: Match exact season number.  
Example: `episode = 13` 
</dd></dl>
<dl>
<dt>container</dt>
<dd>
Options: `AVI, MKV, VOB, MPEG, MP4, ISO, WMV, TS, M4V, M2TS`  
</dd></dl>
<dl>
<dt>codec</dt>
<dd>
Options: `XViD, x264, MPEG2, DiVX, DVDR, VC-1, h.264, WMV, BD, x264-Hi10P`  
</dd></dl>
<dl>
<dt>source</dt>
<dd>
Options:  `HDTV, PDTV, DSR, DVDRip, TVRip, VHSRip, Bluray, BDRip, BRRip, DVD5, DVD9, HDDVD, WEB-DL, WEBRip BD5, BD9, BD25, BD50, Mixed, Unknown`
</dd></dl>
<dl>
<dt>resolution</dt>
<dd>
Options: `SD, 720p, 1080p, 1080i, Portable Device`
</dd></dl>
<dl>
<dt>scene</dt>
<dd>
Description: Match a scene Release.  
Options: `Yes, No`  
</dd></dl>
<dl>
<dt>fast-torrent</dt>
Description: Match release marked a fast torrent (24mbit or faster)  
Options: `Yes, No`  
</dd></dl>
<dl>
<dt>uploader</dt>
<dd>
Description: Match releases for certain BTN uploader.  
Example: `uploader = AlwaysHigh`    
</dd></dl>
<dl>
<dt>except-tags</dt>
<dd>
Description: Filter out certain keywords in release name.  
example: `except-tags = proper, internal`  
</dd></dl>
<dl>
<dt>release-group</dt>
<dd>
Description: Match releases from certain encode groups.  
Example: `release-group = NTb`
</dd></dl>

### Local Filters
<dl>
<dt>filter</dt>
<dd>
Description: Title of global filter to inherit filter from.  
Example: `filter = 720p WEB-DL, 1080p WEB-DL`
</dd></dl>
<dl>
<dt>save-to</dt>
<dd>
Description: Directory where your series files will be saved. You can have a save-to for each filter used.
Examples:
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
</dd></dl>
<dl>
<dt>enabled</dt>
<dd>
Description: Enabled filter to download matches.  
Option: `Yes, No`
</dd></dl>

