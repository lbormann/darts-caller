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

Supported sound-file-namings for Autodarts-Events:
- 0-180.{wav | mp3}
- playername(s).{wav | mp3}   (Name of Autodarts-player(s))
- yr_2-yr_170.{wav | mp3}   (-PCC / --possible_checkout_call = 1)
- matchon.{wav | mp3}
- matchshot.{wav | mp3}
- gameon.{wav | mp3}
- gameshot.{wav | mp3}
- busted.{wav | mp3}
- playerchange.{wav | mp3}
- {s1-t20}.{wav | mp3}  (-E / --call_every_dart = 1)
- single.{wav | mp3}    (-E / --call_every_dart = 1)   
- singleinner.{wav | mp3}   (-E / --call_every_dart = 1)
- singleouter.{wav | mp3}   (-E / --call_every_dart = 1)
- double.{wav | mp3}    (-E / --call_every_dart = 1)
- triple.{wav | mp3}    (-E / --call_every_dart = 1)
- outside.{wav | mp3}   (-E / --call_every_dart = 1)
- ambient_matchon.{wav | mp3}    (-A / --ambient_sounds > 0.0)
- ambient_matchshot.{wav | mp3}  (-A / --ambient_sounds > 0.0)
- ambient_gameon.{wav | mp3}    (-A / --ambient_sounds > 0.0)
- ambient_gameshot.{wav | mp3}  (-A / --ambient_sounds > 0.0)
- ambient_noscore.{wav | mp3}   (-A / --ambient_sounds > 0.0)
- ambient_50more.{wav | mp3}    (-A / --ambient_sounds > 0.0)
- ambient_100more.{wav | mp3}   (-A / --ambient_sounds > 0.0)
- ambient_120more.{wav | mp3}   (-A / --ambient_sounds > 0.0)
- ambient_150more.{wav | mp3}   (-A / --ambient_sounds > 0.0)
- ambient_180.{wav | mp3}   (-A / --ambient_sounds > 0.0)

Since Version 1.6.0 you can deposit multiple sounds for EVERY game-event. Therefor you have to add a "+" to the filename. After the "+" you can add whatever text you prefer; as an example: let`s say we want multiple sounds for the 'gameon'-event. Our default file is 'gameon.mp3/gameon.wav'. Now we add some more: 'gameon+1.mp3', 'gameon+2.mp3', 'gameon+BEST.mp3'. You are not limited to gameon, even score-sounds can have multiple soundfiles.


### App starts and stops immediately?!

Check your autodarts-credentials (use email-adress and password). 
If your are facing "failed keycloakautentikation Error", you probably need to disable Two-Factor-Auth!

### Sound is not playing?!

Sometimes there are sounds that are not readable. In this case you can convert the sound-file(s) with an additional program (https://www.heise.de/download/product/mp3-quality-modifier-66202)
Make sure you configurate 44100HZ, Stereo

### Sound does not match up calls?!
Try https://www.audacity.de/ to modify your sound-files.


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

- -U / --autodarts_email [REQUIRED]
- -P / --autodarts_password [REQUIRED]
- -B / --autodarts_board_id [REQUIRED]
- -M / --media_path [REQUIRED]
- -V / --caller_volume [OPTIONAL] [Default: 1.0] [Possible values: 0.0 .. 1.0]
- -R / --random_caller [OPTIONAL] [Default: 0] [Possible values: 0 | 1]
- -L / --random_caller_each_leg [OPTIONAL] [Default: 0] [Possible values: 0 | 1]
- -E / --call_every_dart [OPTIONAL] [Default: 0] [Possible values: 0 | 1]
- -PCC / --possible_checkout_call [OPTIONAL] [Default: 1] [Possible values: 0 | 1]
- -A / --ambient_sounds [OPTIONAL] [Default: 0.0] [Possible values: 0.0 | 1.0]
- -HP / --host_port [OPTIONAL] [Default: 8079]



#### **-U / --autodarts_email**

You should know your autodarts.io registered email-adress.

#### **-P / --autodarts_password**

You should know your autodarts.io registered password.

#### **-B / --autodarts_board_id**

You should know your autodarts.io registered board-ID (You can find it in Board-Manager).

#### **-M / --media_path**

You need to set an absolut Path to your media-file-directory, otherwise you won`t notice any calls. Make sure your sound-files are in a supported format (mp3,wav).

#### **-V / --caller_volume**

You can lower the call-volume in relation to current system-volume. 1.0 is system-volume. 0.5 is "half" volume. By default this is 1.0

#### **-R / --random_caller**

If you set this to 1 you will get a random caller each time you start the application. For this to work you need to setup subfolders in your media_path. Each subfolder represents an individual caller. By default this is not activated.

#### **-L / --random_caller_each_leg**

If you set this to 1 you will get a random caller each time a new leg starts. By default this is not activated.

#### **-E / --call_every_dart**

If you set this to 1 the caller calls every dart. Setup sounds {S1-T180}, single, double and others. By default this is not activated.

#### **-PCC / --possible_checkout_call**

If you set this to 1 the caller will call if there is a checkout possibility. Setup sounds {playername}{yr_2-yr_170} or {1-170} as a fallback. By default this is activated.

#### **-A / --ambient_sounds**

If you set this to value between 0.1 and 1.0 the caller will call extra sounds like crowd-shouting or whatever you like (you decide!). Setup sounds {ambient_*}. 
The configured value will be multiplied by caller_volume. As an example: caller_volume = 0.8 and ambient_sounds = 1.0 means your sound-volume will be 0.8 relative to your system-volume. By default this is 0.0

#### **-HP / --host_port**

The app provides a websocket-service. Other extensions like autodarts-extern or autodarts-wled can connect to this service (ws://ip:port).
For a list of json-examples look at 'broadcast-examples.dat' - who knows maybe you build your own extension upon this?!




## HELPERS

If you think it is terrible to configure/start/handling this application then go for autodarts-desktop https://github.com/Semtexmagix/autodarts-desktop


## BUGS

It may be buggy. I've just coded it for fast fun with https://autodarts.io. You can give me feedback in Discord > wusaaa


## TODOs

- Support other games modes
- add Readme-section for updating
- add debug by argument
- -E 25 will be called as 25 (that is wrong)
- cricket 2 players 2x gameon
- cricket: do not call marked fields, only call number if field is still open

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



## LAST WORDS

Make sure your speakers are turned on ;)
Thanks to Timo for awesome https://autodarts.io. It will be huge!

