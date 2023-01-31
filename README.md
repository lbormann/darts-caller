# AUTODARTS-CALLER

Autodarts-caller plays sound-files on your local system accordingly to the state of an https://autodarts.io game. Furthermore it can forward game events to other web-applications like https://github.com/lbormann/autodarts-extern that process the incoming data to automate other web-dart-platforms like https://lidarts.org


Tested on Windows 11 Pro x64, Python 3.9.7 and Raspberry pi 4B 4GB, Python 3.9.7


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
| Count Up | o |


## INSTALL INSTRUCTION

### Windows

- Download the executable in the release section.


### Linux / Others

#### Setup python3

- Download and install python 3.x.x for your specific os.
- Download and install pip


#### Get the project

    git clone https://github.com/lbormann/autodarts-caller.git

Go to download-directory and type:

    pip install -r requirements.txt

(Optional) When you encounter problems with playing sound:

    sudo apt-get install python3-sdl2


## SETUP SOUNDS

You need to have sounds-files as mp3 or wav. This files have to be named by 1 to 180, gameshot, busted, playerchange etc. You dont need all files. If you are too lazy you can go for 40, 60, 180 or whatever you like. You can record your voice or download some files in the internet, ie. https://freesound.org or https://www.zapsplat.com
Put all sound files in one folder and if you like create subfolders in this folder for random caller functionality.

Supported sound-file-namings:
- 0-180.{wav | mp3}
- yr_1-yr_170.{wav | mp3}   (YOU REQUIRE)
- gameon.{wav | mp3}
- gameshot.{wav | mp3}
- busted.{wav | mp3}
- playerchange.{wav | mp3}
- single.{wav | mp3}
- double.{wav | mp3}
- triple.{wav | mp3}
- missed.{wav | mp3}




## RUN IT

### Run by executable (Windows)

Create a shortcut of the executable; right click on the shortcut -> select properties -> add arguments in the target input at the end of the text field.

Example: C:\Downloads\autodarts-caller.exe -U "your-autodarts-email" -P "your-autodarts-password" -B "your-autodarts-board-id" -M "absolute-folder-to-your-media-files"

Save changes.
Click on the shortcut to start the caller.


### Run by source

    python autodarts-caller.py -U "your-autodarts-email" -P "your-autodarts-password" -B "your-autodarts-board-id" -M "absolute-folder-to-your-media-files" -V "0.75" -R "0|1" -L "0|1"


### Setup autoboot [linux] (optional)

    crontab -e

At the end of the file add:

    @reboot sleep 30 && cd <absolute-path-to>/autodarts-caller && python autodarts-caller.py -U "TODO" -P "TODO" -B "TODO" -M "TODO"

Make sure you add an empty line under the added command.

Save and close the file. 

Reboot your system.

### Arguments

- -U / --autodarts_email [Required]
- -P / --autodarts_password [Required]
- -B / --autodarts_board_id [Required]
- -M / --media_path [Required]
- -V / --caller_volume [Optional] [Default: 1.0] [Possible values: 0.0 .. 1.0]
- -R / --random_caller [Optional] [Default: 0] [Possible values: 0 | 1]
- -L / --random_caller_each_leg [Optional] [Default: 0] [Possible values: 0 | 1]
- -E / --call_every_dart [Optional] [Default: 0] [Possible values: 0 | 1]
- -PCC / --possible_checkout_call [optional] [Default: 1] [Possible values: 0 | 1]
- -WTT / --webhook_throw_points [Optional] [Default: None]

Some infos about -WTT:
The program tries to request the given url (GET-Request).

Example: if you set -WTT "http://localhost:8080/throw"
the program will extend it internally to "http://localhost:8080/throw/thrower/throw-number/throw-points/points-left/busted/variant" and sends it to the given application (http://localhost:8080)


## EXTENSIONS

If you think it is terrible to configure/start/handling this application then go for autodarts-desktop https://github.com/Semtexmagix/autodarts-desktop


## BUGS

It may be buggy. I've just coded it for fast fun with https://autodarts.io. You can give me feedback in Discord > wusaaa


## TODOs
- Support other games modes (currently only X01 support)
- dont care about last slash in webhook
- add Readme-section for updating
- fix webhook for apps that need info of every throw
- call opponment`s throw
- offer multiple WTT`s


### Done
- Prevent from double calling
- only one webhook with all information (to prevent race condition on receiving app): leg_end, turn, throw_number, throw_value, points_left, variant, user
- let the user configure caller-volume
- Sounds for every throw (single, double, tripple, missed)
- add start argument for surpressing checkout calls
- add sites for free sound-file downloads
- Cricket: Change call behaviour to default
- improved possible checkout call for bogey numbers
- added sound-check on program start
- yr_2-yr_170.{wav | mp3} different sounds-files for possible checkout calls
- Fix sound-play repetition

## LAST WORDS

Make sure your speakers are turned on ;)
Thanks to Timo for awesome https://autodarts.io. It will be huge!

