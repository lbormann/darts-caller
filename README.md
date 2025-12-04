# DARTS-CALLER
[![Downloads](https://img.shields.io/github/downloads/lbormann/darts-caller/total.svg)](https://github.com/lbormann/darts-caller/releases/latest)

Darts-caller plays back sound-files accordingly to the state of a https://autodarts.io game. Furthermore it acts as a central hub by forwarding game-events to connected clients like https://github.com/lbormann/darts-extern that process incoming data to automate other dart-web-platforms like https://lidarts.org.

Learn more about the [Features!](#workflow--functionality)

> [!IMPORTANT]
> CALLER VERSION BELOW v2.8.0 WILL NOT WORK ANYMORE AFTER MIDDLE OF MAY 2025

## COMPATIBILITY

| Variant | Support |
| ------------- | ------------- |
| X01 | :heavy_check_mark: |
| Cricket | :heavy_check_mark: |
| Bermuda | :heavy_check_mark: |
| Shanghai | :heavy_check_mark: |
| Gotcha | :heavy_check_mark: |
| Around the Clock | :heavy_check_mark: |
| Round the World | :heavy_check_mark: |
| Random Checkout | :heavy_check_mark: |
| Count Up | :heavy_check_mark: |
| Segment Training | |
| Bobs 27 | |

<div style="display: flex;">
  <h2> Preview - Web-Caller </h2>
  <img src="https://github.com/lbormann/darts-caller/blob/master/images/chat.jpg" alt="chat preview 1" style="width:250px;margin-right:15px;margin-top:15px;"/>
  <img src="https://github.com/lbormann/darts-caller/blob/master/images/chat2.jpg" alt="chat preview 2" style="width:250px;margin-right:15px;margin-top:15px;"/>
  <img src="https://github.com/lbormann/darts-caller/blob/master/images/chat3.jpg" alt="chat preview 3" style="width:250px;margin-right:15px;margin-top:15px;"/>
</div>


## INSTALL INSTRUCTION

### Desktop-OS:

- If you're running a desktop-driven OS it's recommended to use [darts-hub](https://github.com/lbormann/darts-hub) as it takes care of starting, updating, configurating and managing multiple apps.


### Headless-OS:

- Download the appropriate executable in the release section.


### By Source:
> [!NOTE]
> running by source i supported again since v2.19.0

Setup python3

- Download and install python 3.x.x for your specific os.


#### Get the project

    git clone https://github.com/lbormann/darts-caller.git

Go to download-directory and type:

    pip3 install -r requirements.txt

Optional for Linux: If you encounter problems local playback:

    sudo apt-get install python3-sdl2



## WORKFLOW & FUNCTIONALITY

The following section elucidates the procedure and individual components of the application with the aim that you gain a better understanding upon reading.


### Downloads & Voice-packs

After launching the application, "voice-packs" are automatically downloaded. A voice-pack represents a specific speaker, comprised of a collection of audio files. These audio files can be accessed by the application to announce your scored points. The application features a wide variety of voice-packs, encompassing different languages and genders. 
Due to the potentially lengthy process of downloading and extracting all voice-packs, the number of downloads is initially limited to a small selection of English-speaking speakers. However, you can lift this restriction. During the download phase, there is no calling functionality. Returning to the definition of a "voice-pack": it contains all the audio files necessary to ensure a complete "calling experience." Each audio file within it is named according to a specific schema, enabling the application to recognize the content (or intended content) based on the file name. For instance, the file "gameon.mp3" contains an audio track where the speaker announces the start of the game. If, hypothetically, this file were renamed "game.mp3," the application would fail to interpret it since the content association would be lost. "gameon" serves as a valid "sound-file-key," whereas "game" does not. The application is equipped with an extensive repertoire of valid [SOUND-FILE-KEYS](#SOUND-FILE-KEYS). 
The available voice-packs for download are periodically expanded, such as with the addition of new audio files for player names (gathered separately through a process on autodarts.io). If you're interested in knowing how to ensure your player name is included in future voice-packs, please read the [rules](https://discord.com/channels/802528604067201055/1146376616264597647/1148254133963477044) on Discord and adjust your name accordingly.


### How can I add sounds to a voice-pack?

Every downloaded voice-pack contain all sound-files of category 'MAIN', 'LOBBY', 'SINGLE-DART-SCORE' and 'SINGLE-DART-NAME'. So you're good to go without the need to add extra sounds.
If you would like to extend a voice-pack, for example to add sound-files-keys of category 'AMBIENT' like "ambient_gameshot" or "ambient_playerchange", copy them into --media_path_shared (-MS) to make them usable for every voice-pack.
In addition you can place multiple sounds for a sound-file-key. Therefor you have to add a "+" to the filename. After the "+" you can add whatever text you prefer; as an example: let`s say we want multiple sounds for the 'ambient_gameshot' sound-file-key. Our default file is 'ambient_gameshot.mp3'. Now we add some more: 'ambient_gameshot+1.mp3', 'ambient_gameshot+2.mp3', 'ambient_gameshot+BEST.mp3'. This logic is not limited to the "ambient_gameshot" sound-file-key - this logic applies to every sound-file-key.


### How can I add my own voice-pack?

Create or copy a folder in the path you defined for -M (--media_path) containing every sound-file-key you wish to be included. Make sure you follow the [rules of valid SOUND-FILE-KEYS](#SOUND-FILE-KEYS).
It is advantageous for the folder to adhere to the naming convention. For example: "en-gb-russ-bray-male" (country-region-name-gender).




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







### SOUND-FILE-KEYS

***EVERY SOUND-FILE NEEDS TO BE .mp3 or .wav***


**LOBBY**

- {playername}
- average
- 0-180
- left

**MAIN:**

- hi
- {playername} (-CCP > 0)
- bulling_start
- bulling_end
- gameon
- matchon
- gameshot
- gameshot_l{x}_n
- matchshot
- matchcancel
- leg_{x}
- set_{x}
- s{x}_l{x}_n
- busted
- 0-180
- c_2-c_170 (-PCC > 0)
- you_require (-PCC > 0)
- yr_2-yr_170 (-PCC > 0) [fallback for 'you_require']
- first_to_throw

**SINGLE-DART-SCORE (Argument -E = 1):**

- 0-60

**SINGLE-DART-NAME (Argument -E = 2):**

- bull
- bullseye
- 1-20
- s1-s20 [overrides: 1-20]
- double
- d1-d20 [overrides: double 1-20]
- triple
- t1-t20 [overrides: triple 1-20]
- outside
- m1-m20 [overrides: outside]

**SINGLE-DART-EFFECT (Argument -E = 3):**

- effect_single 
- effect_singleinner [overrides: effect_single]
- effect_singleouter [overrides: effect_single]
- effect_bull [overrides: effect_single]
- effect_s1-effect_s20 [overrides: effect_single, effect_singleinner, effect_singleouter]
- effect_double
- effect_bullseye [overrides: effect_double]
- effect_d1-effect_d20 [overrides: effect_double]
- effect_triple
- effect_t1-effect_t20 [overrides: effect_triple]
- effect_outside
- effect_m1-effect_m20 [overrides: effect_outside]

**AMBIENT (Argument -A > 0.0):**

- ambient_lobby_in
- ambient_lobby_out
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
- ambient_matchcancel
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
- ambient_bogey_number
- ambient_bogey_number_{bogey_number} [overrides: ambient_bogey_number]

**ATC (Around the clock)**

- atc_target_hit
- atc_target_missed
- atc_target_next

**RTW (Round the world)**

- rtw_target_hit_single
- rtw_target_hit_double
- rtw_target_hit_triple
- rtw_target_missed

**Bermuda**

- ber_minus

**Gotcha**

- got_score_denied

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

Example: C:\Downloads\darts-caller.exe -U "your-autodarts-email" -P "your-autodarts-password" -B "your-autodarts-board-id" -M "absolute-path-to-your-media-files"

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


#### *`-U / --autodarts_email`*

<p>**REQUIRED:** 
Your autodarts.io registered email-address.</p>

#### *`-P / --autodarts_password`*

<p>**REQUIRED:** 
Your autodarts.io registered password. Make sure you disable 2FA (Two-Factor-Auth).</p>

#### *`-B / --autodarts_board_id`*

<p>**REQUIRED:** 
Your autodarts.io registered board-id. You can find your Board-ID in Board-Manager.</p>

#### *`-M / --media_path`*

<p>**REQUIRED:** 
Setup an absolute-path where voice-packs should be located.

Make sure the given path doesn't reside inside main-directory (darts-caller).

Examples: 
- (Windows): C:\Users\Luca\Desktop\Programme\autodarts\darts-caller-speaker
- (Linux): /home/luca/autodarts/darts-caller-speaker

Side note: this folder will be targeted for voice-pack-downloads/installs (-DL).</p>


#### *`-MS / --media_path_shared`*

<p>If you do not want to configure same sounds again for every individual voice-pack, you can specify an absolute path to a shared directory. Every voice-pack will use the sounds of that directory. Have a look at [supported SOUND-FILE-KEYS](#SOUND-FILE-KEYS). Moreover make sure the given path neither resides inside main-directory (darts-caller) nor inside media-path (-M).

Side note: sounds located in that directory will override sounds located in voice-pack(s).</p>

#### *`-V / --caller_volume`*

<p>You can lower the local playback volume in relation to current system volume. 
'1.0' is max volume. '0.5' is "half" volume.

Default: '1.0'

Side note: The web-caller has its own volume control.</p>

#### *`-C / --caller`*

<p>Sets a specific voice-pack as caller. On start the application displays a list of installed voice-packs; copy the name of chosen one and paste it here.

Side note: You can change the caller/voice-pack anytime in the web-caller.</p>

#### *`-R / --random_caller`*

<p>The application will randomly choose a voice-pack. If you use this functionality, the application only considers most recent version of a voice-pack by finding its highest version number by name. Example: 'en-US-Joey-Male-v3'. Because there is no voice-pack with name 'en-US-Joey-Male-v4', version is 'v3' (en-US-Joey-Male-v3).

- '0' = random caller deactivated (instead use -C to set your favorite caller)
  
- '1' = random caller for every match-start
  
- '2' = random caller for every leg

Default: '1'</p>

#### *`-CRL / --caller_real_life`*

<p>The caller switches to more realistic announcements to get the feeling of a real stage caller. More reference is made to the players, especially during leg or set changes. Still in the testing phase!</p>

#### *`-RL / --random_caller_language`*

<p>Filters randomly chosen voice-pack by its language.

- '0' = every language
- '1' = english
- '2' = french
- '3' = russian
- '4' = german
- '5' = spanish
- '6' = dutch

Default: '1'

Side note: You can change that option anytime in the web-caller.</p>

#### *`-RG / --random_caller_gender`*

<p>Filters randomly chosen voice-pack by its gender.

- '0' = every gender
- '1' = female
- '2' = male

Default: '0'

Side note: You can change that option anytime in the web-caller.</p>

#### *`-CCP / --call_current_player`*

<p> The application will call playernames for certain events like 'you require' 'legset start' 'legset end'.

- '0' = call current playername deactivated
  
- '1' = call current playername activated
  
- '2' = call current playername activated also on every playerchange

Default: '1'

Side note: You can change that option anytime in the web-caller. </p>

#### *`-CBA / --call_bot_actions`*

<p>The application will call bot actions.

- '0' = call bot actions deactivated
  
- '1' = call bot actions activated

Default: '1'

Side note: You can change that option anytime in the web-caller.</p>

#### *`-E / --call_every_dart`*

<p>The application will call every thrown dart.

- '0' = call every dart deactivated
 
- '1' = SINGLE-DART-SCORE: call every dart by multiplicated score of field-number and field-multiplier (for example: you hit a triple 20, resulting in calling sound-file-key '60')
 
- '2' = SINGLE-DART-NAME: call every dart by field-name (for example: you hit a triple 20, resulting in calling sound-file-key 't20' if available, else falls back to sound-file-key 'triple' and sound-file-key '20')
 
- '3' = SINGLE-DART-EFFECT: call every dart by using sound-effects (for example: you hit a triple 20, resulting in calling sound-file-key 'effect_t20' if available, else falls back to 'effect_triple')

Default: '0'

Side note: You can change that option anytime in the web-caller.</p>

#### *`-ETS / --call_every_dart_total_score`*

<p>The application will call total score if call-every-dart is active ('1', '2', '3').

- '0' = call total score deactivated
  
- '1' = call total score activated

Default: '1'</p>

#### *`-PCC / --possible_checkout_call`*

<p>The application will call and repeat 'x' times a particular checkout until configured value 'x' is reached. 
If configured value 'x' is reached it will playback sound-file-key 'ambient_checkout_call_limit' instead. 
If possible-checkout`s remaining value changes it will call and repeat 'x' times a particular checkout until configured value 'x' is reached.

For playback the application uses two SOUND-FILE-KEYS: 'you_require' and 'c_2-c_170' (fallback to '2-170'). If 'you_require' is not available it will fallback to single sound-file-key: 'yr_2 to yr_170'.

Default: '1' (x = 1 => call a particular possible checkout one time)

Side note: You can change that option anytime in the web-caller.</p>

#### *`-PCCYO / --possible_checkout_call_yourself_only`*

<p>If you set this to '1' the application will only call if there is a checkout possibility and the current player is you (associated to your board-id). 
This functionality won't work if your board is offline.

- '0' = call possible checkout for every player
  
- '1' = call possible checkout only for yourself

Default: '0'

Side note: You can change that option anytime in the web-caller.</p>

#### *`-A / --ambient_sounds`*

<p>If you set this to value between '0.1' and '1.0' the application will playback SOUND-FILE-KEYS ambient_*. 
The configured value will be multiplied by caller-volume (-V). As an example: caller-volume = '0.8' and ambient-sounds = '1.0' resultung in '0.8' relative to your system-volume.</p>


#### *`-AAC / --ambient_sounds_after_calls`*

<p>If you set this to '1', SOUND-FILE-KEYS ambient_* will wait until main-calls are finished.

Default: '0'</p>

#### *`-DL / --downloads`*

<p>The application will download 'x' available voice-packs that are not already installed. Installation path is the value of -M. 

Default: '3'</p>

#### *`-DLLA / --downloads_language`*

<p>If you want to filter downloads for a specific language.

- '0' = every language
- '1' = english
- '2' = french
- '3' = russian
- '4' = german
- '5' = spanish
- '6' = dutch

Default: '1'</p>

#### *`-DLN / --downloads_name`*

<p>If you want to filter downloads to a specific voice-pack. For example you could set a value 'en-US-Joey-Male'.</p>

#### *`-ROVP / --remove_old_voice_packs`*

<p>The application will remove old voice-packs folders from your disk.

Default: '0'</p>

#### *`-BAV / --background_audio_volume`*

<p>You can not hear any calls as your music is way too loud? Try to set this to '0.03'.

Default: '0.0' (no background-audio-muting)

Side Note: only availble for windows-os and local playback (LPB = 1).</p>

#### *`-LPB / --local_playback`*

<p>The application will playback audio by using your local speakers.

Default: '1'</p>

#### *`-WEBDH / --web_caller_disable_https`*

<p>If you set this to '1' the application will run all connection services with insecure http/ws protocol. It's NOT recommended! 
Also you won't be able to use video-/voice-calls on web-caller.

Default: '0'</p>

#### *`-HP / --host_port`*

<p>The application provides a websocket-service. Other extensions like darts-extern or darts-wled can connect to this service (wss://ip:port).
For a list of json-examples look at 'broadcast-examples.dat' - who knows maybe you build your own extension upon this?!

Default: '8079'</p>

#### *`-DEB / --debug`*

<p>The application outputs extended event-information.

Default: '0'</p>


### Blind Support Feature, extended Callouts

#### *`-CBS / --call_blind_support`*

<p>Enables blind support mode for visually impaired players. When activated, the caller announces the target field at the beginning of each turn (for applicable game modes) and provides detailed information about where each dart landed.

Supported game modes: X01, Around the Clock (ATC), Round the World (RTW), Bermuda, Shanghai, Count-Up, and Gotcha.

Features:
- Target announcements at turn start (e.g., "Target is triple 20" for ATC)
- Dart position announcements after each throw
- require announcements after each throw if in checkout area
- Replaces standard calling when enabled to prevent duplicate announcements

Required sound files:
- bs_target_is: "Target is" announcement
- bs_single_inner: For inner single announcements
- bs_any_double: For "any double" targets (Bermuda)
- bs_any_triple: For "any triple" targets (Bermuda)
- Existing t*, d*, m* files for triple/double/miss announcements

- '0' = blind support deactivated
- '1' = blind support activated

Default: '0'
</p>



### Setup autostart [linux] (optional)

There are endless possibilities to manage an autostart. You find two ways to do it (both using the start-custom.sh to run it by source)

#### Using a cronjob

    crontab -e

At the end of the file add (Replace USER):

    @reboot sleep 30 && cd /home/USER/darts-caller && ./start-custom.sh > /home/USER/darts-caller.log 2>&1

Reboot your system:

    sudo reboot

Check log:

    tail /home/USER/darts-caller.log






#### Using a desktop-start-task (linux with gui only)

if you are facing problems with the crontab-solution try this:

    sudo apt install xterm

One can now manually test whether the whole thing starts with the following command (adjust USER):

    xterm -e "cd /home/USER/darts-caller && ./start-custom.sh"

A terminal-like window should now open with the running program.

To enable autostart, a .desktop file now needs to be created:

    sudo nano ~/.config/autostart/dartscaller.desktop

Insert the following into this file and adjust the USER in the path:

    [Desktop Entry]
    Type=Application
    Exec=xterm -e "cd /home/USER/darts-caller && ./start-custom.sh > /home/USER/darts-caller.log 2>&1"
    Hidden=false
    NoDisplay=false
    X-GNOME-Autostart-enabled=true
    X-GNOME-Autostart-Delay=10
    Name[de_DE]=Darts-Caller
    Name=Darts-Caller
    Comment[de_DE]=Autostart Darts-Caller
    Comment=Autostart Darts-Caller

Afterwards, save the file (Ctrl + O) and close the file (Ctrl + X).

Now the file permissions need to be set for the file (again, adjust USER!):

    sudo chmod u=rw-,g=rw-,o=r-- ~/.config/autostart/dartscaller.desktop
    sudo chmod +x ~/.config/autostart/dartscaller.desktop
    sudo chown USER ~/.config/autostart/dartscaller.desktop

Reboot your system:

    sudo reboot

Check log:

    tail /home/USER/darts-caller.log



## Docker:
To install the caller inside a docker container, use a compose file that looks like this:
```yml
version: '3.3'

services:
  darts-caller:
    image: lbormann/darts-caller
    container_name: darts-caller
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
    - ./darts-caller/media:/usr/share/darts-caller/media
    - ./darts-caller/media-shared:/usr/share/darts-caller/media-shared
    - ./darts-caller:/usr/share/darts-caller
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
- Make sure your email-address ist correct.
- Make sure your password ist correct. (Else: try to change your password)

### Can not play sound for sound-file-key 'X' -> Ignore this or check existance; otherwise convert your file appropriate

This is NOT automatically an error. It just informs you about a missing sound-file-key.
If you wish to hear that missing sound-file-key, make sure the audio file exists.
If you rename any of your sound-files while the application is running you need to restart the application to apply changes.

### Sound is not playing?!

- Check if the filename exists on your drive
- Check that the filename is a supported [Sound-file-key](#SOUND-FILE-KEYS)
- Sometimes there are sounds that are not playable. In this case you can convert that sound-file with the help of an additional program like (https://www.heise.de/download/product/mp3-quality-modifier-66202) Make sure you configurate 44100HZ, Stereo.
- Check the console output: in case you do not receive any messages (only 'Receiving live information from ..') -> you should check the given Board-ID (-B) for correctness.

### I don't like sound X of voice-pack Y

EVERY sound-file is optional! If you don't like a specific sound just delete it! The application can even function with no files at all.

### I don't like voice-pack X

There are multiple ways to ban an undesired voice-pack:

- Option 1) Visit web-caller and press "Ban Caller!"
- Option 2) Delete ALL audio-files of voice-pack-folder.
- Option 3) use [darts-voice](https://github.com/lbormann/darts-voice).

All options forcing the application to either download files again nor using a voice-pack for calling.
If you wish to revoke a ban, open 'banned.txt' and remove the line from the list.

### App starts and stops immediately?!

Start application out of terminal to check whats going on.

### Sound does not match up calls?!
Try https://www.audacity.de/ to modify your sound-files.

## Where can I download additional sounds?

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
    All other filled columns (separated by semicolon ';') specify [SOUND-FILE-KEYS](#SOUND-FILE-KEYS) that are used by darts-caller.
    For an example have a look at 'en-US-v1.csv' template.

    - **Sounds archive:**
    A ZIP file (*.zip) (filename: "{speaker name}"-"{m|f}"-"{language}".zip - for example: "max-m-german.zip"). This ZIP-file must contain a folder (filename irrelevant). The folder contains the sound-files. It should be noted that the sounds-files MUST be in the same order (when sorted alphabetically) as listed in the template-file; however, the actual filename is completely irrelevant.

    - **Source file (optional but desirable):**
    A text file (*.txt) (filename: irrelevant) containing additional information about the origin of the sound files.
    For example you could mention a link where the sounds were generated; a specification of generation-parameters and so on.

2) Upload the ZIP archive to a file-hoster: Make sure you choose a filehoster that supports direct-links and UNLIMITED file-persistence without restrictions (GoogleDrive, OneDrive, ...). !!IMPORTANT!! Before you upload, check if you are eligible to distribute the sound-files - Are you the owner? Are you allowed to share it in public?

3) Sent me a your link by PM on Discord - Wait for a new release :) 

## STATISTICS
The darts caller collects data and stores it in a database. The data is NOT sold or used for advertising purposes. The reason for the data collection is to continuously develop the caller, to have the user settings for debugging purposes and to get an overview of which features are used and worth developing further. 

All arguments are collected except for user sensitive data such as e-mail address, password, board or UserID. 

With the increasing number of users >2000 we want to create a possibility to provide faster support. This collection enables us to see directly which settings may be incorrect and could lead to a problem. 

None of this data will be passed on to third parties!


## RESOURCES

- Sounds by <a href="https://zapsplat.com">zapsplat.com</a>
- Icon by <a href="https://freeicons.io/user-interface-and-electronics/camera-cam-photo-pic-shoot-image-ui-f-ef-ec-icon-841">icon king1</a>
- Icon by <a href="https://freeicons.io/office-and-workstation-icons-6/video-call-icon-19057">Free Preloaders</a>
- Icon by <a href="https://freeicons.io/undefined/star-icon-14946">Free Icons Pack</a>
