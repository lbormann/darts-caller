# AUTODARTS-CALLER
[![Downloads](https://img.shields.io/github/downloads/lbormann/autodarts-caller/total.svg)](https://github.com/lbormann/autodarts-caller/releases/latest)

Autodarts-caller plays back sound-files accordingly to the state of a https://autodarts.io game. Furthermore it acts as a central hub by forwarding game-events to connected clients like https://github.com/lbormann/autodarts-extern that process incoming data to automate other dart-web-platforms like https://lidarts.org.

Learn more about the [Features!](#workflow--functionality)


## COMPATIBILITY

| Variant | Support |
| ------------- | ------------- |
| X01 | :heavy_check_mark: |
| Cricket | :heavy_check_mark: |
| Bermuda | |
| Shanghai | |
| Gotcha | |
| Around the Clock | :heavy_check_mark: |
| Round the World | :heavy_check_mark: |
| Random Checkout | :heavy_check_mark: |
| Count Up | |
| Segment Training | |

<div style="display: flex;">
  <h2> Preview - Web-Caller </h2>
  <img src="https://github.com/lbormann/autodarts-caller/blob/master/images/chat.jpg" alt="chat preview 1" style="width:250px;margin-right:15px;margin-top:15px;"/>
  <img src="https://github.com/lbormann/autodarts-caller/blob/master/images/chat2.jpg" alt="chat preview 2" style="width:250px;margin-right:15px;margin-top:15px;"/>
  <img src="https://github.com/lbormann/autodarts-caller/blob/master/images/chat3.jpg" alt="chat preview 3" style="width:250px;margin-right:15px;margin-top:15px;"/>
</div>


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

Optional for Linux: If you encounter problems local playback:

    sudo apt-get install python3-sdl2



## WORKFLOW & FUNCTIONALITY

The following section elucidates the procedure and individual components of the application with the aim that you gain a better understanding upon reading.


### Downloads & Voice-packs

After launching the application, "voice-packs" are automatically downloaded. A voice-pack represents a specific speaker, comprised of a collection of audio files. These audio files can be accessed by the application to announce your scored points. The application features a wide variety of voice-packs, encompassing different languages and genders. 
Due to the potentially lengthy process of downloading and extracting all voice-packs, the number of downloads is initially limited to a small selection of English-speaking speakers. However, you can lift this restriction. During the download phase, there is no calling functionality. Returning to the definition of a "voice-pack": it contains all the audio files necessary to ensure a complete "calling experience." Each audio file within it is named according to a specific schema, enabling the application to recognize the content (or intended content) based on the file name. For instance, the file "gameon.mp3" contains an audio track where the speaker announces the start of the game. If, hypothetically, this file were renamed "game.mp3," the application would fail to interpret it since the content association would be lost. "gameon" serves as a valid "sound-file-key," whereas "game" does not. The application is equipped with an extensive repertoire of valid [sound-file-keys](#Sound-file-keys). 
The available voice-packs for download are periodically expanded, such as with the addition of new audio files for player names (gathered separately through a process on autodarts.io). If you're interested in knowing how to ensure your player name is included in future voice-packs, please read the [rules](https://discord.com/channels/802528604067201055/1146376616264597647/1148254133963477044) on Discord and adjust your name accordingly.


### How can I add sounds to a voice-pack?

Every voice-pack contain all sound-files of category 'MAIN' and 'LOBBY'. So you're good to go by default without changing anything.
If you would like to extend a voice-pack, for example to add sound-files-keys of category 'AMBIENT' like "ambient_gameshot" or "ambient_playerchange", copy them into --media_path_shared (-MS) to make them usable for every voice-pack.
In addition you can place multiple sounds for a sound-file-key. Therefor you have to add a "+" to the filename. After the "+" you can add whatever text you prefer; as an example: let`s say we want multiple sounds for the 'ambient_gameshot' sound-file-key. Our default file is 'ambient_gameshot.mp3'. Now we add some more: 'ambient_gameshot+1.mp3', 'ambient_gameshot+2.mp3', 'ambient_gameshot+BEST.mp3'. Of course you are not limited to the "ambient_gameshot" sound-file-key - this rule applies to every sound-file-key.


### How can I add my own voice-pack?

Create a folder in path you defined for -M (--media_path) containing every audio file you wish to be included. Make sure you follow the [rules of valid sound-file-keys](#Sound-file-keys).
It is advantageous for the folder to adhere to the naming convention. For example: "en-GB-russ-bray-male" (country-region-name-gender).




### Web-Caller

The web-caller provides various functionalities on a website hosted locally on your end. By default you can access this website on any device with a modern browser by entering https://your-ip:8079. 
Contrary to what the name 'Web-Caller' might suggest, it offers more than just the pure "call functionality".
The website is divided into the following sections or functionalities:

#### Start

* By pressing the start button, you enable the browser to play audio files and initiate the connection to the application.

#### Chat

- Automatically generated peer-to-peer chat with your opponent.
- Exchange of text-based messages, links, and images.
- Quick message storage function (e.g., to send emojis directly via a dedicated button).
- Voice- and video-calls (requires active HTTPS).

Disclaimer: In order for the chat window to appear, your opponent must have the web caller open. Additionally, chatting with multiple players is currently not possible (only in 1v1, game variant: X01).

#### Calling

- Direct audio playback through a browser of your choice (the current voice-pack is downloaded or updated and then cached to enable seamless playback for later visits).
- Display of the current speaker (voice-pack).
- Selection menu to switch to a specific speaker.
- Button to switch to another random speaker.
- Selection menus for adjusting language and gender.
- Button to ban the current speaker.
- Button to favor the current speaker (Favoured speakers will be color-coded and positioned at the top of the selection list).
- Button to introduce the current speaker.
- Mod section:
    - adjust arguments on-the-fly
    - customize current speaker voice

Disclaimer: For uninterrupted calling experience on mobile devices, ensure that your device display remains active while you are playing.

#### Board

- Button for automatic calibration of your board
- Button for resetting your board

#### Game

- "Magic button" for automatic transitioning between lobby, turns, and games, depending on the current status of the match.







### Sound-file-keys

***EVERY SOUND-FILE NEEDS TO BE .mp3 or .wav***

**MAIN:**

- bulling_start
- bulling_end
- gameon
- matchon
- gameshot
- matchshot
- matchcancel
- leg_{x}
- set_{x}
- busted
- 0-180
- {playername} (-CCP > 0)
- you_require (-PCC = 1 and -PCCSF = 0)
- yr_2-yr_170 (-PCC = 1 and -PCCSF = 1)

**LOBBY**

- {playername}
- average
- 0-180
- left

**SINGLE-DART-SOUND-EFFECTS (Argument -E = 2):**

- single 
- singleinner [overrides: single]
- singleouter [overrides: single]
- double
- triple
- s1-s20 [overrides: single, singleinner, singleouter]
- d1-d20 [overrides: double]
- t1-t20 [overrides: triple]
- sbull [overrides: single]
- bull [overrides: double]
- outside

**AMBIENT (Argument -A > 0.0):**

- ambient_playerchange
- ambient_playerchange_{playername} [overrides: ambient_playerchange]
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
- ambient_lobby_in
- ambient_lobby_out

**ATC (Around the clock)**

- atc_target_hit
- atc_target_missed
- atc_target_next

**RTW (Round the world)**

- rtw_target_hit_single
- rtw_target_hit_double
- rtw_target_hit_triple
- rtw_target_missed

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

Example: C:\Downloads\autodarts-caller.exe -U "your-autodarts-email" -P "your-autodarts-password" -B "your-autodarts-board-id" -M "absolute-path-to-your-media-files"

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
- -R / --random_caller [Default: 1] [Possible values: 0 | 1 | 2]
- -RL / --random_caller_language [Default: 1] [Possible values: look at description below]
- -RG / --random_caller_gender [Default: 0] [Possible values: look at description below]
- -CCP / --call_current_player [Default: 1] [Possible values: 0 | 1 | 2]
- -E / --call_every_dart [Default: 0] [Possible values: 0 | 1 | 2]
- -ETS / --call_every_dart_total_score [Default: 1] [Possible values: 0 | 1]
- -PCC / --possible_checkout_call [Default: 1] [Possible values: 0..Inf]
- -PCCSF / --possible_checkout_call_single_files [Default: 1] [Possible values: 0 | 1]
- -PCCYO / --possible_checkout_call_yourself_only [Default: 0] [Possible values: 0 | 1]
- -A / --ambient_sounds [Default: 0.0] [Possible values: 0.0 .. 1.0]
- -AAC / --ambient_sounds_after_calls [Default: 0] [Possible values: 0 | 1]
- -DL / --downloads [Default: 1] [Possible values: 0 | 1]
- -DLL / --downloads_limit [Default: 3]
- -DLLA / --downloads_language [Default: 1] [Possible values: look at description below]
- -DLN / --downloads_name [Default: '']
- -BAV / --background_audio_volume [Default: 0.0] [Possible values: 0.0 .. 1.0]
- -LPB / --local_playback [Default: 1] [Possible values: 0 | 1]
- -WEBDH / --web_caller_disable_https [Default: 0] [Possible values: 0 | 1]
- -HP / --host_port [Default: 8079]
- -DEB / --debug [Default: 0] [Possible values: 0 | 1]



#### **<span style="color:red">`-U / --autodarts_email`</span>**

You should know your autodarts.io registered email-address.

#### **`-P / --autodarts_password`**

You should know your autodarts.io registered password. Make sure you disable 2FA (Two-Factor-Auth).

#### **`-B / --autodarts_board_id`**

You can find your Board-ID in Board-Manager.

#### **`-M / --media_path`**

Setup an absolute-path where voice-packs should be located. Just create an empty folder.
Make sure the given path doesn't reside inside main-directory (autodarts-caller).

Examples: 
- (Windows): C:\Users\Luca\Desktop\Programme\autodarts\autodarts-caller-speaker
- (Linux): /home/luca/autodarts/autodarts-caller-speaker

Side note: this folder will be targeted for voice-pack-downloads/installs (-DL).

#### *`-MS / --media_path_shared`*

If you do not want to configure same sounds again for every individual voice-pack, you can specify an absolute path to a shared directory. Every voice-pack will use the sounds of that directory. Have a look at [supported Sound-file-keys](#Sound-file-keys). Moreover make sure the given path neither resides inside main-directory (autodarts-caller) nor inside media-path (-M).

[Default: '']

Side note: sounds located in that directory will override sounds located in voice-pack(s).

#### *`-V / --caller_volume`*

You can lower the call-volume in relation to current system-volume. '1.0' is system-volume. '0.5' is "half" volume.

[Default: 1.0] [Possible values: 0.0 .. 1.0]

Side note: The web-caller has its own volume control.

#### *`-C / --caller`*

Sets a specific voice-pack as caller. On start the application displays a list of installed voice-packs; copy the name of chosen one and paste it here. By default this is 'None' meaning the application chooses a random caller (voice-pack).

Side note: You can change the caller/voice-pack anytime in the web-caller.

#### *`-R / --random_caller`*

The application will randomly choose a voice-pack. If you use this functionality, the application only considers most recent version of a voice-pack by finding its highest version number by name. Example: 'en-US-Joey-Male-v3'. Because there is no voice-pack with name 'en-US-Joey-Male-v4', version is 'v3' (en-US-Joey-Male-v3). By default this is '1'.

- '0' = random caller deactivated (instead use -C to set your favorite caller)
- '1' = random caller for every match-start
- '2' = random caller for every leg

#### *`-RL / --random_caller_language`*

Filters randomly chosen voice-pack by its language. '0' means no filtering (every language). By default this is '1' (english).

- '0' = every language
- '1' = english
- '2' = french
- '3' = russian
- '4' = german
- '5' = spanish
- '6' = dutch

Side note: You can change the gender anytime in the web-caller.

#### *`-RG / --random_caller_gender`*

Filters randomly chosen voice-pack by its gender. '0' means no filtering (every gender). By default this is '0'.

- '0' = every gender
- '1' = female
- '2' = male

Side note: You can change the gender anytime in the web-caller.

#### *`-CCP / --call_current_player`*

The application will call playernames for certain events like "you require", "leg/set start", "leg/set end". By default this is activated.

- '0' = call current playername deactivated
- '1' = call current playername activated
- '2' = call current playername also on every playerchange

Side note: You can change that option anytime in the web-caller.

#### *`-E / --call_every_dart`*

The application will call every thrown dart. By default this is not activated.

- '0' = call every dart deactivated
- '1' = call every dart by calculating the multiplication of field value and multiplier (for example: you hit a triple 20, resulting in calling 60). 
- '2' = call every dart by calling sound-effects you setup. s1, d1, t1 to s20, d20, t20, outside, sbull, bull. If particular sound-file-key can't be found, it will fallback to: singleinner, singleouter, single, double, triple.

Side note: You can change that option anytime in the web-caller.

#### *`-ETS / --call_every_dart_total_score`*

The application will call total score if call-every-dart is active (1 or 2).
By default this is activated.

#### *`-PCC / --possible_checkout_call`*

If you set this to '1' the application will call possible checkouts. Setup sounds {playername}{yr_2-yr_170} or {2-170} as a fallback. 
If you set this to value above '1' calls won't be repeat when the count of value is reached.
By default this is '1'.

Side note: You can change that option anytime in the web-caller.

#### *`-PCCSF / --possible_checkout_call_single_file`*

If you set this to '0' (default) the application uses two separated sound-files named: 'you_require' and 'x' (score-value). If you set this to '1' the application will call a possible checkout by using one file 'yr_2-yr_170'.

#### *`-PCCYO / --possible_checkout_call_yourself_only`*

If you set this to '1' the application will only call if there is a checkout possibility and the current player is you (associated to your board-id). 
Note: this functionality won't work if your board is offline.
By default this is '0'.

Side note: You can change that option anytime in the web-caller.

#### *`-A / --ambient_sounds`*

If you set this to value between '0.1' and '1.0' the caller will call extra sounds like crowd-shouting or whatever you like (you decide!). Setup sounds {ambient_*}. 
The configured value will be multiplied by caller_volume. As an example: caller_volume = '0.8' and ambient_sounds = '1.0' means your sound-volume will be 0.8 relative to your system-volume. By default this is '0'.

#### *`-AAC / --ambient_sounds_after_calls`*

If you set this to '1' ambient_*-sounds will wait until main-calls are finished. By default this is not activated.

#### *`-DL / --downloads`*

If you set this to '1' the application will download available voice-packs that are not already installed. Installation path is the value of -M. 
By default this is activated.

#### *`-DLL / --downloads_limit`*

If you want to limit download-count, you can set it to x most recent. By default this is '3'.

#### *`-DLLA / --downloads_language`*

If you want to filter downloads for a specific language. '0' means no language-filtering (every language). By default this is '1' (english).

- '0' = every language
- '1' = english
- '2' = french
- '3' = russian
- '4' = german
- '5' = spanish
- '6' = dutch

#### *`-DLN / --downloads_name`*

If you want to filter downloads to a specific voice-pack-name. '' means no name-filtering. By default this is ''.
For example you could set a value 'en-US-Joey-Male'.

#### *`-BAV / --background_audio_volume`*

You can not hear any calls as your music is way too loud? Try to set this to '0.03' and let the calls begin :) Default is '0.0' (no background-audio-muting). Note: Only availble for windows-os and local playback (LPB = 1).

#### *`-LPB / --local_playback`*

If you set this to '1' the application will playback audio by using your local speakers.
By default this is activated.

#### *`-WEBDH / --web_caller_disable_https`*

If you set this to '1' the application will run all connection services with insecure http/ws protocol. It's NOT recommended! 
Also you won't be able to use video-/voice-calls on web-caller.
By default this is not activated.

#### *`-HP / --host_port`*

The application provides a websocket-service. Other extensions like autodarts-extern or autodarts-wled can connect to this service (wss://ip:port).
For a list of json-examples look at 'broadcast-examples.dat' - who knows maybe you build your own extension upon this?!

#### *`-DEB / --debug`*

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
    - 8079:8079 #Host Port
    devices:
    - /dev/snd:/dev/snd
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

### failed keycloakauthentication Error (401 invalid_grant)

- Disable Two-Factor-Auth (2FA).
- Make sure you use your email-addres.
- Check your password.
- Else try to change your password.

### Can not play sound for sound-file-key 'X' -> Ignore this or check existance; otherwise convert your file appropriate

This is NOT automatically an error. It just informs you about a missing sound-file-key.
If you wish to hear that missing sound-file-key, make sure the audio file exists.
If you rename any of your sound-files while the application is running you need to restart the application to apply changes.

### Sound is not playing?!

- Check if the filename exists on your drive
- Check that the filename is a supported [Sound-file-key](#Sound-file-keys)
- Sometimes there are sounds that are not playable. In this case you can convert that sound-file with the help of an additional program like (https://www.heise.de/download/product/mp3-quality-modifier-66202) Make sure you configurate 44100HZ, Stereo.
- Check the console output: in case you do not receive any messages (only 'Receiving live information from ..') -> you should check the given Board-ID (-B) for correctness.

### I don't like sound X of voice-pack Y

EVERY sound-file is optional! If you don't like a specific sound just delete it! The application can even function with no files at all.

### I don't like voice-pack X

There are multiple ways to ban an undesired voice-pack:

- Option 1) Visist web-caller and press "Ban Caller!"
- Option 2) Delete ALL audio-files of voice-pack-folder.
- Option 3) use [autodarts-voice](https://github.com/lbormann/autodarts-voice).

All options forcing the application to either download files again nor using a voice-pack for calling.
If you wish to revoke a ban, open 'autodarts-caller-banned.txt' and remove the line from the list.

### App starts and stops immediately?!

Start application out of terminal to check whats going on.

### Sound does not match up calls?!
Try https://www.audacity.de/ to modify your sound-files.

## Where can I find additional sounds for ambient or every-dart-sound-effects?

- https://www.101soundboards.com/
- https://freesound.org
- https://www.zapsplat.com
- https://mixkit.co/free-sound-effects/hit/



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


## RESOURCES

- Sounds by <a href="https://zapsplat.com">zapsplat.com</a>
- Icon by <a href="https://freeicons.io/user-interface-and-electronics/camera-cam-photo-pic-shoot-image-ui-f-ef-ec-icon-841">icon king1</a>
- Icon by <a href="https://freeicons.io/office-and-workstation-icons-6/video-call-icon-19057">Free Preloaders</a>
- Icon by <a href="https://freeicons.io/undefined/star-icon-14946">Free Icons Pack</a>