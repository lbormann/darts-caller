# AUTODARTS-CALLER

Autodarts-caller plays sound-files on your local system accordingly to the state of an https://autodarts.io game. Furthermore it acts as a central hub by forwarding game-events to connected clients like https://github.com/lbormann/autodarts-extern that process the incoming data to automate other web-dart-platforms like https://lidarts.org


Tested on Windows 10 & 11 Pro x64, Python 3.9.7 and Raspberry pi 4B 4GB, Python 3.9.7


## COMPATIBILITY

x = supported
o = not (yet) supported

| Variant | Support |
| ------------- | ------------- |
| X01 | x |
| Cricket | x |
| Bermuda | o |
| Shanghai | o |
| Gotcha | o |
| Around the Clock | o |
| Round the World | o |
| Random Checkout | x |
| Count Up | o |


## INSTALL INSTRUCTION

### Windows

- Download the executable in the release section.


### Linux / Others

#### Setup python3

- Download and install python 3.x.x for your specific os.
- Download and install pip.


#### Get the project

    git clone https://github.com/lbormann/autodarts-caller.git

Go to download-directory and type:

    pip install -r requirements.txt

(Optional) When you encounter problems with playing sound:

    sudo apt-get install python3-sdl2


## SETUP SOUNDS

You need to have sounds-files as mp3 or wav. This files have to be named by 1 to 180, gameshot, busted, playerchange etc. You dont need all files. If you are too lazy you can go for 40, 60, 180 or whatever you like. You can record your voice or download some files in the internet, ie. https://freesound.org, https://www.zapsplat.com or watchout for pinned messages in (Discord https://discord.com/channels/802528604067201055/955745166134747196 or https://discord.com/channels/802528604067201055/1019720832647434320).
Put all sound files in one folder and if you like create subfolders in this folder for random caller functionality.

***EVERY SOUND FILE NEEDS TO BE .mp3 or .wav***

**MAIN-CALLING:**

- gameon
- matchon
- gameshot
- matchshot
- busted
- 0-180
- {playername(s)} (Name of Autodarts-player(s) | bot lvl 1-11)
- you_require (-PCC = 1 and -PCCSF = 0)
- yr_2-yr_170 (-PCC = 1 and -PCCSF = 1)
- playerchange

**SINGLE-DARTS (Argument -E = 1):**

- single 
- singleinner [overrides single]
- singleouter [overrides single]
- double
- triple
- outside
- sbull
- bull
- s1-t20 [overrides single, singleinner, singleouter, double, triple]

**AMBIENT (Argument -A > 0.0):**

- ambient_matchon  
- ambient_matchshot
- ambient_gameon  
- ambient_gameshot
- ambient_noscore 
- ambient_50more  
- ambient_100more 
- ambient_120more 
- ambient_150more 
- ambient_180 

______

Since Version 1.6.0 you can deposit multiple sounds for EVERY game-event. Therefor you have to add a "+" to the filename. After the "+" you can add whatever text you prefer; as an example: let`s say we want multiple sounds for the 'gameon'-event. Our default file is 'gameon.mp3/gameon.wav'. Now we add some more: 'gameon+1.mp3', 'gameon+2.mp3', 'gameon+BEST.mp3'. You are not limited to gameon, even score-sounds can have multiple soundfiles.





## RUN IT

### Run by executable (Windows)

Create a shortcut of the executable; right click on the shortcut -> select properties -> add arguments in the target input at the end of the text field.

Example: C:\Downloads\autodarts-caller.exe -U "your-autodarts-email" -P "your-autodarts-password" -B "your-autodarts-board-id" -M "absolute-folder-to-your-media-files"

Save changes.
Click on the shortcut to start the caller.


### Run by source

    python3 autodarts-caller.py -U "your-autodarts-email" -P "your-autodarts-password" -B "your-autodarts-board-id" -M "absolute-folder-to-your-media-files"


### Setup autoboot [linux] (optional)

    crontab -e

At the end of the file add:

    @reboot sleep 30 && cd <absolute-path-to>/autodarts-caller && python3 autodarts-caller.py -U "TODO" -P "TODO" -B "TODO" -M "TODO"

Make sure you add an empty line under the added command.

Save and close the file. 

Reboot your system.

### Arguments

**Required:**

- -U / --autodarts_email
- -P / --autodarts_password
- -B / --autodarts_board_id
- -M / --media_path

**Optional:**

- -MS / --media_path_shared [Default: '']
- -V / --caller_volume [Default: 1.0] [Possible values: 0.0 .. 1.0]
- -C / --caller [Default: None] [Possible values: look at description below]
- -R / --random_caller [Default: 0] [Possible values: 0 | 1]
- -L / --random_caller_each_leg [Default: 0] [Possible values: 0 | 1]
- -E / --call_every_dart [Default: 0] [Possible values: 0 | 1]
- -ESF / --call_every_dart_single_files [Default: 1] [Possible values: 0 | 1]
- -PCC / --possible_checkout_call [Default: 1] [Possible values: 0 | 1]
- -PCCSF / --possible_checkout_call_single_files [Default: 1] [Possible values: 0 | 1]
- -A / --ambient_sounds [Default: 0.0] [Possible values: 0.0 .. 1.0]
- -ACC / --ambient_sounds_after_calls [Default: 0] [Possible values: 0 | 1]
- -DL / --downloads [Default: 1] [Possible values: 0 | 1]
- -DLL / --downloads_limit [Default: 0] [Possible values: 0 .. 1000]
- -DLP / --downloads_path [Default: 'download']
- -HP / --host_port [Default: 8079]



#### **-U / --autodarts_email**

You should know your autodarts.io registered email-adress.

#### **-P / --autodarts_password**

You should know your autodarts.io registered password. Make sure you disable 2FA (Two-Factor-Auth).

#### **-B / --autodarts_board_id**

You can find your Board-ID in Board-Manager.

#### **-M / --media_path**

You need to set an absolute Path to your media-file-directory, otherwise you won`t notice any calls. Make sure your sound-files are in a supported file-format (mp3,wav).

#### **-MS / --media_path_shared**

If you do not want to configure particular sounds for every individual caller, you can specify an absolute path to a shared directory. Every caller will get the sounds of that directory. Have a look at https://github.com/lbormann/autodarts-caller#setup-sounds for supported sound-file-names.

#### **-V / --caller_volume**

You can lower the call-volume in relation to current system-volume. '1.0' is system-volume. '0.5' is "half" volume. By default this is '1.0'

#### **-C / --caller**

Sets a specific caller. On start the application displays a list of installed callers; copy the name of chosen one and paste it here. By default this is 'None' meaning the application will use the sound-files of argument '-M' or a random caller if this is configurated (see next). 

#### **-R / --random_caller**

If you set this to '1' you will get a random caller each time you start the application. For this to work you need to setup subfolders in your media_path. Each subfolder represents an individual caller. By default this is not activated.

#### **-L / --random_caller_each_leg**

If you set this to 1' you will get a random caller each time a new leg starts. By default this is not activated.

#### **-E / --call_every_dart**

If you set this to '1' the caller calls every dart. Setup sounds 's1'-'t20', single, double and others. This is pretty handy if you want to play sound-effects. (https://github.com/lbormann/autodarts-caller#setup-sounds) Note: the third dart will never trigger any extra sound as there are more important events, like summed score, busted etc.

#### **-ESF / --call_every_dart_single_files**

If you set this to '0' the application calls every dart by combining the type of hit (single, double ..) with hit-number (20, 30, ..) so that it reuses
the sounds of score-values (0-180). If you set this to '1' (default) it will call by using only one file (ie. single, double, t19, ..).

#### **-PCC / --possible_checkout_call**

If you set this to '1' the caller will call if there is a checkout possibility. Setup sounds {playername}{yr_2-yr_170} or {2-170} as a fallback. By default this is activated.

#### **-PCCSF / --possible_checkout_call_single_file**

If you set this to '0' (default), the application uses two separated sound-files named: 'you_require' and 'x' (score-value). If you set this to '1' the application will call a possible checkout by using one file 'yr_2-yr_170'.  

#### **-A / --ambient_sounds**

If you set this to value between '0.1' and '1.0' the caller will call extra sounds like crowd-shouting or whatever you like (you decide!). Setup sounds {ambient_*}. 
The configured value will be multiplied by caller_volume. As an example: caller_volume = '0.8' and ambient_sounds = '1.0' means your sound-volume will be 0.8 relative to your system-volume. By default this is '0'.

#### **-ACC / --ambient_sounds_after_calls**

If you set this to '1' ambient_*-sounds will wait until main-calls are finished. By default this is not activated.

#### **-DL / --downloads**

If you set this to '1' the application will download all possible caller-voices that are not already installed. By default this is activated.

#### **-DLL / --downloads_limit**

If you wish to stop the application from checking/downloading all possible caller-voices, you can limit it to x most recent. By default this is '0' (no limit).

#### **-DLP / --downloads_path**

In case you face problems with caller-voices-downloads try to change the download-path (absolute Path). By default this is 'download' in the application`s directory.

#### **-HP / --host_port**

The app provides a websocket-service. Other extensions like autodarts-extern or autodarts-wled can connect to this service (ws://ip:port).
For a list of json-examples look at 'broadcast-examples.dat' - who knows maybe you build your own extension upon this?!

## FAQ

### App starts and stops immediately?!

Check your autodarts-credentials (use email-adress and password). 
If your are facing "failed keycloakauthentication Error (401 invalid_grant)", you probably need to disable Two-Factor-Auth!

### Sound is not playing?!

Sometimes there are sounds that are not readable. In this case you can convert the sound-file(s) with an additional program (https://www.heise.de/download/product/mp3-quality-modifier-66202)
Make sure you configurate 44100HZ, Stereo

### Sound does not match up calls?!
Try https://www.audacity.de/ to modify your sound-files.


## CONTRIBUTE

### Do you want to provide your caller profile to the community?

Here are the two steps to do that!


1) Create a ZIP archive that contains the following contents:

**Template file:**
A UTF8-encoded CSV file (*.csv) with a BOM (filename can be chosen freely), which is structured as follows:
Column 1 contains the phrase to be translated into the respective language by the provider. For example: "The game is over."
All further columns (separated by semicolon ';') contain "caller-filename-keys".
All valid keys can be viewed at https://github.com/lbormann/autodarts-caller#setup-sounds.
Finished templates for multiple languages can be found in the caller-templates folder.

**Sounds archive:**
A ZIP file (*.zip) (filename: "{speaker name}"-"{m|f}"-"{language}".zip - for example: "Max-m-deutsch.zip") containing a folder with the sound files. It should be noted that the sounds MUST be in the same order (when sorted alphabetically) as in the template file; however, the actual filename is completely irrelevant.

**Source file (optional but desirable):**
A text file (*.txt) (filename: freely chosen) containing additional information about the origin of the sound files.
Examples: Link to the website where the sounds were generated; specific generation profile for this speaker during generation.


2) Upload your files to a file-hoster: Make sure you choose a filehoster that supports direct-links and unlimited file-persistence wihout restrictions (mediafire.com is a good hoster for that). 
!! IMPORTANT!! Before you upload, check your rights regarding distribution of your sound-files; are you the owner? Are you allowed to share it in public?

3) Sent me a PM on Discord with the download-link (direct link) - Wait for an caller-update :) 



## HELPERS

If you think it is terrible to configure/start/handling this application then go for autodarts-desktop https://github.com/Semtexmagix/autodarts-desktop


## BUGS

It may be buggy. I've just coded it for fast fun with https://autodarts.io. You can give me feedback in Discord > wusaaa


## TODOs

- Support other games modes
- add Readme-section for updating
- add debug by argument
- cricket 2 players 2x gameon
- cricket: do not call marked fields, only call number if field is still open
- add example start-command to RM (win/linux)
- Bots no dart-sounds for every turn (at least not for ESF = 0)


### Done

- Prevent from double calling
- only one webhook with all information (to prevent race condition on receiving app): leg_end, turn, throw_number, throw_value, points_left, variant, user
- let the user configure caller-volume
- Sounds for every throw (single, double, tripple, missed)
- add start argument for surpressing checkout calls
- add sites for free sound-file downloads
- Cricket: Change call behaviour to default
- improved possible checkout call for bogey numbers
- yr_2-yr_170.{wav | mp3} different sounds-files for possible checkout calls
- Fix sound-play repetition
- Improved error logging
- dont care about last slash in webhook
- fix webhook for apps that need info of every throw
- offer multiple WTT`s
- add [playername] to gameshot like in [playername] you require
- add configurable pygame.mixer
- add possibility to have more sound-files for one event (random if multiple found)
- add ambient-sounds for gameon, gamewon, noscore etc.
- call every field possible
- added matchshot
- use WS
- -E 25 will be called as 25 (that is wrong)
- improve console logs
- add caller-profile-downloader
- add ambient_sounds_common_media_path
- add every_single_dart_common_media_path



## LAST WORDS

Make sure your speakers are turned on ;)
Thanks to Timo for awesome https://autodarts.io. It will be huge!

