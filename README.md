# AUTODARTS-CALLER
[![Downloads](https://img.shields.io/github/downloads/lbormann/autodarts-caller/total.svg)](https://github.com/lbormann/autodarts-caller/releases/latest)

Autodarts-caller plays back sound-files accordingly to the state of a https://autodarts.io game. Furthermore it acts as a central hub by forwarding game-events to connected clients like https://github.com/lbormann/autodarts-extern that process incoming data to automate other dart-web-platforms like https://lidarts.org


## COMPATIBILITY

| Variant | Support |
| ------------- | ------------- |
| X01 | :heavy_check_mark: |
| Cricket | :heavy_check_mark: |
| Bermuda | |
| Shanghai | |
| Gotcha | |
| Around the Clock | :heavy_check_mark: |
| Round the World | |
| Random Checkout | :heavy_check_mark: |
| Count Up | |
| Segment Training | |


## INSTALL INSTRUCTION

### Desktop-OS:

- If you're running a desktop-driven OS it's recommended to use [autodarts-desktop](https://github.com/lbormann/autodarts-desktop) as it takes care of starting, updating, configurating and managing multiple apps.


### Headless-OS:

- Download the appropriate executable in the release section.


### By Source:

#### Setup python3

- Download and install python 3.x.x for your specific os.


#### Get the project

    git clone https://github.com/lbormann/autodarts-caller.git

Go to download-directory and type:

    pip3 install -r requirements.txt

Optional for Linux: If you encounter problems with playing sound:

    sudo apt-get install python3-sdl2



## SETUP

Since version 2.0.0 there is a build-in download-mechanismn that automatically downloads multiple voice-packs in different languages and genders on application start - you don't need to setup manually. Every voice-pack contain all sound-files of category [MAIN-CALLING](#Sound-file-keys). If you would like to extend a voice-pack, e.g. to add other sound-files-keys like "ambient_gameshot" or "ambient_playerchange", copy them into specific voice-pack directory to use them only for specific voice-pack or copy them into --media_path_shared (-MS) to use them for every voice-pack. You can find a specific voice-pack in --media_path (-M).

### Use my own voice-pack / sounds

Copy your sound-files to --media_path (-M). Make sure your sound-files are named according to the rules: [supported sound-file-keys](#Sound-file-keys). You don't need to have all listed sound-file-keys - just add the ones you want to use.
You can find sounds at https://freesound.org, https://www.zapsplat.com, https://mixkit.co/free-sound-effects/hit/. 

______

Since Version 1.6.0 you can deposit multiple sounds for every ([sound-file-key](#Sound-file-keys)). Therefor you have to add a "+" to the filename. After the "+" you can add whatever text you prefer; as an example: let`s say we want multiple sounds for the 'gameon'-event. Our default file is 'gameon.mp3'. Now we add some more: 'gameon+1.mp3', 'gameon+2.mp3', 'gameon+BEST.mp3'. You are not limited to the gameon-event, even score-sounds can have multiple soundfiles.



### Sound-file-keys

***EVERY SOUND-FILE NEEDS TO BE .mp3 or .wav***

**MAIN:**

- gameon
- matchon
- gameshot
- matchshot
- matchcancel
- leg_{x}
- set_{x}
- busted
- 0-180
- {playername} (-CCP = 1)
- you_require (-PCC = 1 and -PCCSF = 0)
- yr_2-yr_170 (-PCC = 1 and -PCCSF = 1)

**SINGLE-DARTS (Argument -E = 1):**

- single 
- singleinner [overrides: single]
- singleouter [overrides: single]
- double
- triple
- outside
- s1-s20 [overrides: single, singleinner, singleouter]
- d1-d20 [overrides: double]
- t1-t20 [overrides: triple]
- sbull [overrides: single]
- bull [overrides: double]

**AMBIENT (Argument -A > 0.0):**

- ambient_playerchange
- ambient_gameon 
- ambient_gameon_{playername} [overrides: ambient_gameon]
- ambient_matchon
- ambient_matchon_{playername} [overrides: ambient_matchon]  
- ambient_gameshot
- ambient_gameshot_{playername} [overrides: ambient_gameshot]
- ambient_setshot
- ambient_setshot_{playername} [overrides: ambient_setshot] 
- ambient_matchshot
- ambient_matchshot_{playername} [overrides: ambient_matchshot]
- ambient_bogey_number
- ambient_noscore
- ambient_1more
- ambient_50more  
- ambient_100more 
- ambient_120more 
- ambient_150more 
- ambient_1-ambient_180 [overrides: ambient_Xmore]
- ambient_{any 3 darts combo, for example "t1s1d1"} [overrides: ambient_1-ambient_180]
- ambient_group_legendary
- ambient_group_perfect
- ambient_group_very_nice
- ambient_group_good
- ambient_group_normal
- ambient_checkout_call_limit

**LOBBY**

- lobby_ambient_in
- lobby_ambient_out
- lobby_player
- lobby_average
- lobby_left

**ATC (Around the clock)**

- atc_target_hit
- atc_target_missed
- atc_target_next

**CONTROL**

- control
- control_next [overrides: control]
- control_next_game [overrides: control]
- control_undo [overrides: control]
- control_ban_caller [overrides: control]
- control_change_caller [overrides: control]
- control_calibrate [overrides: control]
- control_dart_correction [overrides: control]
- control_dart_correction_1 [overrides: control, control_dart_correction]
- control_dart_correction_2 [overrides: control, control_dart_correction]
- control_dart_correction_3 [overrides: control, control_dart_correction]





## RUN IT

You can run by source or run an os-specific executable (recommended).


### Run by executable

#### Example: Windows 

Create a shortcut of the executable; right click on the shortcut -> select properties -> add [Arguments](#Arguments) in the target input at the end of the text field.

Example: C:\Downloads\autodarts-caller.exe -U "your-autodarts-email" -P "your-autodarts-password" -B "your-autodarts-board-id" -M "absolute-folder-to-your-media-files"

Save changes.
Click on the shortcut to start the application.


### Run by source

#### Example: Linux

Copy the default script:

    cp start.sh start-custom.sh

Edit and fill out [Arguments](#Arguments):

    nano start-custom.sh

Make it executable:

    chmod +x start-custom.sh

Start the script:

    ./start-custom.sh



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
- -R / --random_caller [Default: 1] [Possible values: 0 | 1]
- -L / --random_caller_each_leg [Default: 0] [Possible values: 0 | 1]
- -RL / --random_caller_language [Default: 1] [Possible values: 0 (every language) | 1 (english) | 2 (french) | 3 (russian) | 4 (german) | 5 (spanish) | 6 (dutch)]
- -RG / --random_caller_gender [Default: 0] [Possible values: 0 (every gender) | 1 (female) | 2 (male) ]
- -CCP / --call_current_player [Default: 1] [Possible values: 0 | 1]
- -CCPA / --call_current_player_always [Default: 0] [Possible values: 0 | 1]
- -E / --call_every_dart [Default: 0] [Possible values: 0 | 1]
- -ESF / --call_every_dart_single_files [Default: 1] [Possible values: 0 | 1]
- -PCC / --possible_checkout_call [Default: 1] [Possible values: 0..Inf]
- -PCCSF / --possible_checkout_call_single_files [Default: 1] [Possible values: 0 | 1]
- -PCCYO / --possible_checkout_call_yourself_only [Default: 0] [Possible values: 0 | 1]
- -A / --ambient_sounds [Default: 0.0] [Possible values: 0.0 .. 1.0]
- -AAC / --ambient_sounds_after_calls [Default: 0] [Possible values: 0 | 1]
- -DL / --downloads [Default: 1] [Possible values: 0 | 1]
- -DLL / --downloads_limit [Default: 0]
- -DLLA / --downloads_language [Default: 1] [Possible values: 0 (every language) | 1 (english) | 2 (french) | 3 (russian) | 4 (german) | 5 (spanish) | 6 (dutch)]
- -DLN / --downloads_name [Default: '']
- -BLP / --blacklist_path [Default: '']
- -BAV / --background_audio_volume [Default: 0.0] [Possible values: 0.0 .. 1.0]
- -WEB / --web_caller [Default: 0] [Possible values: 0,1,2]
- -WEBSB / --web_caller_scoreboard [Default: 0] [Possible values: 0 | 1]
- -WEBP / --web_caller_port [Default: 5000]
- -HP / --host_port [Default: 8079]
- -DEB / --debug [Default: 0] [Possible values: 0 | 1]



*`-U / --autodarts_email`*

You should know your autodarts.io registered email-adress.

*`-P / --autodarts_password`*

You should know your autodarts.io registered password. Make sure you disable 2FA (Two-Factor-Auth).

*`-B / --autodarts_board_id`*

You can find your Board-ID in Board-Manager.

*`-M / --media_path`*

Setup an absolute path where sounds should be/are located (If you are new just create an empty folder for that).
Examples: 
- (Windows): C:\Users\Luca\Desktop\Programme\autodarts\autodarts-caller-speaker
- (Linux): /home/luca/autodarts/autodarts-caller-speaker

By-the-way: this folder will be targeted for voice-pack-downloads/installs (-DL).
Make sure the given path doesn't reside inside main-directory (autodarts-caller).

*`-MS / --media_path_shared`*

If you do not want to configure same sounds again for every individual voice-pack, you can specify an absolute path to a shared directory. Every voice-pack will use the sounds of that directory. Have a look at [supported Sound-file-keys](#Sound-file-keys). Moreover make sure the given path neither resides inside main-directory (autodarts-caller) nor inside media-path (-M).

*`-V / --caller_volume`*

You can lower the call-volume in relation to current system-volume. '1.0' is system-volume. '0.5' is "half" volume. By default this is '1.0'.

*`-C / --caller`*

Sets a specific voice-pack as caller. On start the application displays a list of installed voice-packs; copy the name of chosen one and paste it here. By default this is 'None' meaning the application uses sound-files of argument '-M' or a random voice-pack if this is configurated (see next). Note: if you set this to a value unequal to 'None' the arguments '-R' and '-L' are no more relevant.

*`-R / --random_caller`*

The application will randomly choose a voice-pack on every match-start. If you use this functionality, the application considers only most recent version of a voice-pack by finding highest version number (e.g: a-caller-v3).
By default this is activated.

*`-L / --random_caller_each_leg`*

If you set this to '1' the application will randomly choose a voice-pack each time a new leg starts. By default this is not activated.

*`-RL / --random_caller_language`*

Filters randomly chosen voice-pack by its language. '0' means no filtering. By default this is '1' (english).

*`-RG / --random_caller_gender`*

Filters randomly chosen voice-pack by its gender. '0' means no filtering. By default this is '0'.

*`-CCP / --call_current_player`*

If you set this to '1' the application will call playernames for certain events like "you require", "leg/set start", "leg/set end". By default this is activated.

*`-CCPA / --call_current_player_always`*

If you set this to '1' the application will call playernames on every playerchange (-CCP needs to be activated). By default this is not activated. 

*`-E / --call_every_dart`*

If you set this to '1' the application calls every thrown dart. Setup sounds 's1'-'t20', single, double and others. This is pretty handy if you want to play sound-effects. Note: the third dart will only considered if argument '-ESF' is set to '1'.

*`-ESF / --call_every_dart_single_files`*

If you set this to '0' the application calls every thrown dart by combining the type of hit (single, double ..) with hit-number (20, 30, ..) so that it reuses
the sounds of score-values (0-180). If you set this to '1' (default) it will call by using only one file (ie. single, double, t19, ..).

*`-PCC / --possible_checkout_call`*

If you set this to '1' the application will call possible checkouts. Setup sounds {playername}{yr_2-yr_170} or {2-170} as a fallback. 
If you set this to value above '1' calls won't be repeat when the count of value is reached.
By default this is '1'.

*`-PCCSF / --possible_checkout_call_single_file`*

If you set this to '0' (default) the application uses two separated sound-files named: 'you_require' and 'x' (score-value). If you set this to '1' the application will call a possible checkout by using one file 'yr_2-yr_170'.

*`-PCCYO / --possible_checkout_call_yourself_only`*

If you set this to '1' the application will only call if there is a checkout possibility and the current player is you (associated to your board-id). 
Note: this functionality won't work if your board is offline.
By default this is '0'.

*`-A / --ambient_sounds`*

If you set this to value between '0.1' and '1.0' the caller will call extra sounds like crowd-shouting or whatever you like (you decide!). Setup sounds {ambient_*}. 
The configured value will be multiplied by caller_volume. As an example: caller_volume = '0.8' and ambient_sounds = '1.0' means your sound-volume will be 0.8 relative to your system-volume. By default this is '0'.

*`-AAC / --ambient_sounds_after_calls`*

If you set this to '1' ambient_*-sounds will wait until main-calls are finished. By default this is not activated.

*`-DL / --downloads`*

If you set this to '1' the application will download available voice-packs that are not already installed. Installation path is the value of -M. 
On first application-start, it downloads and extracts multiple voice-packs: it will take several minutes; be patient - take a coffee. 
By default this is activated.

*`-DLL / --downloads_limit`*

If you want to limit download-count, you can set it to x most recent. By default this is '0' (no limitation).

*`-DLLA / --downloads_language`*

If you want to filter downloads for a specific language. '0' means no language-filtering. By default this is '1' (english).

*`-DLN / --downloads_name`*

If you want to filter downloads to a specific voice-pack-name. '' means no name-filtering. By default this is ''.

*`-BLP / --blacklist_path`*

The blacklist-file stores voice-pack-names that are undesired for downloads or calls. In other words: those ones are just ignored by the application. To use blacklist define an absolute path where the blacklist-file should be located (it will be generated automatically on application start). Now you can simply add an undesired voice-pack-name (have a look at available ones on application start). 

*`-BAV / --background_audio_volume`*

You can not hear any calls as your music is way too loud? Try to set this to '0.03' and let the calls begin :) Default is '0.0' (no background-audio-muting). Note: Only availble on windows-os.

*`-WEB / --web_caller`*

If you set this '1' or '2' the application will host a web-server to mirror call-events. A value '1' will play sounds only on the website. Value '2' will play sounds on the application (locally) and on the website; Use your smartphone, tablet or other device and visit http://{machine-ip-address}:{web-caller-port}. For a continuous calling experience make sure your device display stays on while you are playing. For faster processing the web-caller caches sound-files which results in fast response times; Internet Explorer, non-chromium Edge and Safari > v10 is mandantory as caching is realized by indexeddb.
If you're using an ios device, you probably need to open the page twice and confirm audio-playing by pressing the displayed button. In case that doesn't solve problems try to use another browser like firefox. 

*`-WEBSB / --web_caller_scoreboard`*

If you set this to a '1' the application will host a web-endpoint to display an alternative scoreboard. Visit http://{machine-ip-address}:{web-caller-port}/scoreboard in browser.

*`-WEBP / --web_caller_port`*

If web-calling or web-scoreboard is enabled, you can configure a custom port. By default this is '5000'.

*`-HP / --host_port`*

The application provides a websocket-service. Other extensions like autodarts-extern or autodarts-wled can connect to this service (ws://ip:port).
For a list of json-examples look at 'broadcast-examples.dat' - who knows maybe you build your own extension upon this?!

*`-DEB / --debug`*

Set this to value '1', to output extended event-information on console. By default this is '0'.




### Setup autostart [linux] (optional)

There are endless possibilities to manage an autostart. You find two ways to do it (both using the start-custom.sh to run it by source)

#### Using a cronjob

    crontab -e

At the end of the file add (Replace USER):

    @reboot sleep 30 && cd /home/USER/autodarts-caller && ./start-custom.sh > /home/USER/autodarts-caller.log 2>&1

Reboot your system:

    sudo reboot

Check log:

    tail /home/USER/autodarts-caller.log






#### Using a desktop-start-task (linux with gui only)

if you are facing problems with the crontab-solution try this:

    sudo apt install xterm

One can now manually test whether the whole thing starts with the following command (adjust USER):

    xterm -e "cd /home/USER/autodarts-caller && ./start-custom.sh"

A terminal-like window should now open with the running program.

To enable autostart, a .desktop file now needs to be created:

    sudo nano ~/.config/autostart/autodartscaller.desktop

Insert the following into this file and adjust the USER in the path:

    [Desktop Entry]
    Type=Application
    Exec=xterm -e "cd /home/USER/autodarts-caller && ./start-custom.sh > /home/USER/autodarts-caller.log 2>&1"
    Hidden=false
    NoDisplay=false
    X-GNOME-Autostart-enabled=true
    X-GNOME-Autostart-Delay=10
    Name[de_DE]=Autodarts-Caller
    Name=Autodarts-Caller
    Comment[de_DE]=Autostart Autodarts-Caller
    Comment=Autostart Autodarts-Caller

Afterwards, save the file (Ctrl + O) and close the file (Ctrl + X).

Now the file permissions need to be set for the file (again, adjust USER!):

    sudo chmod u=rw-,g=rw-,o=r-- ~/.config/autostart/autodartscaller.desktop
    sudo chmod +x ~/.config/autostart/autodartscaller.desktop
    sudo chown USER ~/.config/autostart/autodartscaller.desktop

Reboot your system:

    sudo reboot

Check log:

    tail /home/USER/autodarts-caller.log



## Docker:
To install the caller inside a docker container, use a compose file that looks like this:
```yml
version: '3.3'

services:
  autodarts-caller:
    image: lbormann/autodarts-caller
    container_name: autodarts-caller
    restart: unless-stopped
    ports:
    - 5000:5000 #Web Caller Port
    - 8079:8079 #Host Port
    privileged: true
    environment:
      #required settings
      AUTODARTS_EMAIL:    '' #Your autodarts mail adress
      AUTODARTS_PASSWORD: '' #Your autodarts password
      AUTODARTS_BOARD_ID: '' #Your autodarts board id
      
    volumes:
    - ./autodarts-caller/media:/usr/share/autodarts-caller/media
    - ./autodarts-caller/media-shared:/usr/share/autodarts-caller/media-shared
    - ./autodarts-caller:/usr/share/autodarts-caller
```
If you want additional parameters, add them as environment variables:

```yml
environment:
  AUTODARTS_EMAIL:    '' #Your autodarts mail adress
  AUTODARTS_PASSWORD: '' #Your autodarts password
  AUTODARTS_BOARD_ID: '' #Your autodarts board id
  CALLER_VOLUME: 0.5
```

If you wish to no paste your password, consider storing it in a separate .env file. Make sure to secure your env-file (`chmod 600 .env` should be enough)

.env:
```
AUTODARTS_EMAIL=my@email.com
AUTODARTS_PASSWORD=VERYSTRONG
AUTODARTS_BOARD_ID=123-456-789

```


## FAQ

### App has strange behaviour / got an error message

- Enable debug ('-DEB "1"') to display more information about a problem.
- If you don't know how to solve a problem, have a look below.

### Failed to process voice-pack 'X'

All voice-packs are hosted on dropbox. There is a chance that you encounter this error as dropbox allows only a certain download count in unknown time window.
Just be patient, wait a few hours and restart the application. It could be helpful to restart your router or use a vpn to bypass.

### failed keycloakauthentication Error (401 invalid_grant)

- Disable Two-Factor-Auth (2FA).
- Make sure you use your email-addres - NOT your username.
- Check your password.

### Can not play sound for sound-file-key 'X' -> Ignore this or check existance; otherwise convert your file appropriate

Make sure the displayed exists! If you rename any of your sound-files you NEED to restart the application as it internally creates a list of available sound-files ONLY on application-start AND on a caller-switch (random_caller-functionality)!

### Sound is not playing?!

- Check that the filename is a supported [Sound-file-key](#Sound-file-keys)
- Sometimes there are sounds that are not readable. In this case you can convert sound-file(s) with an additional program (https://www.heise.de/download/product/mp3-quality-modifier-66202) Make sure you configurate 44100HZ, Stereo.
- Check the console output: in case you do not receive any messages (only 'Receiving live information from ..') -> you should check the given Board-ID (-B) for correctness.

### I don't like sound X of voice-pack Y

EVERY sound is optional! If you don't like a specific sound just delete it! The application can even function with no files at all.

### I don't like voice-pack X

There are two ways to ban an undesired voice-pack.
Option 1) Delete ALL files of voice-pack-folder.
Option 2) use [autodarts-voice](https://github.com/lbormann/autodarts-voice) to ban the the current caller when he/she is active.
Option 3) put the name of the current caller (voice-pack) in autodarts-caller-banned.txt by yourself.
All 3 options forcing the application to either download files again nor using a voice-pack anymore, except you define it in -C or -DLN
If you wish to revoke a ban, open 'autodarts-caller-banned.txt' and remove the line from the list.

### App starts and stops immediately?!

Start application out of terminal to check whats going on.

### Sound does not match up calls?!
Try https://www.audacity.de/ to modify your sound-files.



## CONTRIBUTE

### Do you want to provide your voice-pack to the community? It`s easy - read on!

1) Create a ZIP archive that contains the following contents:

    - **Template file:**
    A UTF8-(with a BOM)-encoded CSV file (*.csv) (filename irrelevant), which is structured as follows:
    Column 1 contains a phrase that a sound file is based on. For example: "The game is over."
    All other filled columns (separated by semicolon ';') specify [Sound-file-keys](#Sound-file-keys) that are used by autodarts-caller.
    For an example have a look at 'en-US-v1.csv' template.

    - **Sounds archive:**
    A ZIP file (*.zip) (filename: "{speaker name}"-"{m|f}"-"{language}".zip - for example: "max-m-german.zip"). This ZIP-file must contain a folder (filename irrelevant). The folder contains the sound-files. It should be noted that the sounds-files MUST be in the same order (when sorted alphabetically) as listed in the template-file; however, the actual filename is completely irrelevant.

    - **Source file (optional but desirable):**
    A text file (*.txt) (filename: irrelevant) containing additional information about the origin of the sound files.
    For example you could mention a link where the sounds were generated; a specification of generation-parameters and so on.

2) Upload the ZIP archive to a file-hoster: Make sure you choose a filehoster that supports direct-links and UNLIMITED file-persistence without restrictions (GoogleDrive, OneDrive, ...). !!IMPORTANT!! Before you upload, check if you are eligible to distribute the sound-files - Are you the owner? Are you allowed to share it in public?

3) Sent me a your link by PM on Discord - Wait for a new release :) 


## LAST WORDS

Make sure your speakers are turned on ;)
Thanks to Timo for awesome https://autodarts.io. It will be huge!

