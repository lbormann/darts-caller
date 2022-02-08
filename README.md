# AUTODARTS-CALLER

Autodarts-caller plays sound-files on your local system accordingly to the state of an autodarts.io match. You should run this on any machine that supports python. Of course it should be possible to run it next to autodarts itself.
It automatically looks for an active game that is associated with your autodarts board-id.
At the time only the game logic of X01-Variant is supported.
Tested on Windows 11 Pro x64, Python 3.9.7.


## INSTALL INSTRUCTION


### Setup python3

- Download and install python 3.x.x for your specific os.
- Download and install pip


### Get the project

    git clone https://github.com/lbormann/autodarts-caller.git

Go to download-directory and type:

    pip install -r requirements.txt


### Setup media folder

You need sounds-files (mp3 or wav). You should have placed files that are named from 1 to 180, busted, gameshot, required. You dont need all files. If you are too lazy you can go for 40, 60, 180 or whatever you like. You can record your voice or download some files in the internet, ie. freesound.org.
Put all sound files in one folder and if you like create subfolders in this folder for random caller functionality. (use R / --random_caller = 1 - as argument on program start).

Care of file-namings (Currently supported)
- 0-180.{wav | mp3}
- gameon.{wav | mp3}
- gameshot.{wav | mp3}
- busted.{wav | mp3}


## RUN IT

Arguments:
-U / --autodarts_email [Required]
-P / --autodarts_password [Required]
-B / --autodarts_board_id [Required]
-M / --media_path [Required]
-R / --random_caller [Optional][Default: 0]
-L / --random_caller_each_leg [Optional][Default: 0]

Simple run command example:

    python autodarts-caller.py -U <your-autodarts-email> -P <your-autodarts-password> -B <your-autodarts-board-id> -M <absolute-folder-to-your-media-files> -R <0|1> -L <0|1>


## Setup autoboot (optional)

    crontab -e

At the end of the file add:

    @reboot cd <absolute-path-to>/autodarts-caller && python autodarts-caller.py -U <TODO> -P <TODO> -B <TODO> -M <TODO>" 

Save and close the file. Reboot your system.





## BUGS

It may be buggy. I've just coded it for fast fun with autodarts.io. You can give me feedback in Discord > wusaaa


## TODOs

- Make it more easy to use
- Care of possible error situations that may appear during long run 
- Support other games modes (currently only X01 support)


## LAST WORDS

Make sure your speakers are turned on ;)
Thanks to Timo for awesome autodarts.io. It will be huge!

