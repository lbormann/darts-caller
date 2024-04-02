# AUTODARTS-CALLER
[![Downloads](https://img.shields.io/github/downloads/lbormann/autodarts-caller/total.svg)](https://github.com/lbormann/autodarts-caller/releases/latest)

Autodarts-caller plays back sound-files accordingly to the state of a https://autodarts.io game. Furthermore it acts as a central hub by forwarding game-events to connected clients like https://github.com/lbormann/autodarts-extern that process incoming data to automate other dart-web-platforms like https://lidarts.org
Learn more about the [Features!](#WORKFLOW & FUNCTIONALITY)

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

Optional for Linux: If you encounter problems with playing sound:

    sudo apt-get install python3-sdl2



## WORKFLOW & FUNCTIONALITY

Der folgende Abschnitt erklärt den Ablauf und die einzelnen Komponenten der Anwendung mit dem Ziel, dass Du nach dem Lesen ein besseres Verständnis erlangst.

### Downloads & Voice-packs

Nach dem Start der Anwendung, werden automatisch sogenannte "voice-packs" heruntergeladen. Ein voice-pack stellt einen bestimmten Sprecher dar, der aus einer Sammlung von Audio-Dateien besteht. Diese Audio-Dateien können von der Anwendung gelesen werden, um deine geworfenen Punkte ausrufen zu können. Die Anwendung kennt eine große Anzahl, verschiedener voice-packs, bestehend aus unterschiedlichen Sprachen und Geschlechtern. Da das Herunterladen und die Extraction sämtlicher voice-packs sehr lange dauern kann, ist die Anzahl der Downloads standartmäßig auf eine kleine Anzahl englisch-sprachiger Sprecher begrenzt. Diese Begrenzung kannst Du natürlich aufheben (später mehr dazu). Zurück zu der Definition eines "voice-pack": Ein voice-pack enthält alle Audio-Dateien, um ein vollständiges "Call-Erlebnis" zu garantieren. Jede enthaltene Audio-Datei ist nach einem bestimmten Schema benannt, sodass die Anwendung über den Namen einer Datei erkennen kann, welcher Ton-Inhalt vorliegt (vorliegen soll). Ein Beispiel dazu: Datei "gameon.mp3" enthält eine Audiospur, in der der Sprecher zum Spielstart ausruft. Nehmen wir an, diese Datei würde nun nicht mehr "gameon.mp3" heißen, sondern "game.mp3". Dies würde zur Folge haben, dass die Anwendung mit dieser Datei nichts anfangen kann, da eine inhaltliche Zuordnung nicht möglich ist. "gameon" ist ein sogenannter "sound-file-key". "game" ist kein gültiger sound-file-key. Die Anwendung kennt ein großes Repertoire von gültigen [sound-file-keys](#Sound-file-keys). 
Die zum Download, zur Verfügung gestellten voice-packs, werden in unregelmäßigen Abständen erweitert; beispielsweise werden neue Audio-Dateien für Spielernamen (die in einem separaten Prozess auf autodarts.io gesammelt werden) hinzugefügt. Falls Du wissen möchtest, was Du machen musst, damit dein Spielername in zukünftigen voice-packs enthalten ist, ließ Dir bitte folgendes Regelwerk auf Discord durch und passe ggf. deinen Namen an: TODODISCORDLINK



### How can I use my own Sounds?

Every voice-pack contain all sound-files of category [MAIN-CALLING](#Sound-file-keys). If you would like to extend a voice-pack, e.g. to add other sound-files-keys like "ambient_gameshot" or "ambient_playerchange", copy them into specific voice-pack directory to use them only for specific voice-pack or copy them into --media_path_shared (-MS) to use them for every voice-pack. You can find a specific voice-pack in --media_path (-M).

Copy your sound-files to --media_path (-M). Make sure your sound-files are named according to the rules: [supported sound-file-keys](#Sound-file-keys). You don't need to have all listed sound-file-keys - just add the ones you want to use.
You can find sounds at . 

______

Since Version 1.6.0 you can deposit multiple sounds for every ([sound-file-key](#Sound-file-keys)). Therefor you have to add a "+" to the filename. After the "+" you can add whatever text you prefer; as an example: let`s say we want multiple sounds for the 'gameon'-event. Our default file is 'gameon.mp3'. Now we add some more: 'gameon+1.mp3', 'gameon+2.mp3', 'gameon+BEST.mp3'. You are not limited to the gameon-event, even score-sounds can have multiple soundfiles.


Fassen wir also zusammen. In der Theorie kann die Anwendung unendlich viele Sprecher (voice-packs) verarbeiten, wobei jedes voice-pack aus vielen Audio-Dateien besteht, die bestimmtermaßen benannt sein müssen, damit die Verarbeitung dieser funktioniert.





### Web-Caller

Der Web-caller stellt verschiedene Funktionalitäten auf einer, bei Dir lokal gehosteten Website bereit. Diese Website kannst Du auf allen Geräten mit einem modernen Browser aufrufen. Anders als der Name vielleicht vermuten lässt, bietet der Web-Caller mehr als nur die reine "Call-Funktionalität".
Die Webseite ist in folgende Bereiche, bzw. Funktionalitäten aufgeteilt:

#### Start

* Durch Drücken des Start-Knopfs erlaubst Du dem Browser das Abspielen von Audio-Dateien und startest damit auch die Verbindung zur Anwendung.

#### Chat

* Automatisch erzeugter peer-to-peer Chat mit deinem Gegner.
* Austausch von textbasierten Nachrichten, Links und Bildern.
* Schnellspeicher-Funktion für Nachrichten (z.B. um Emotjis direkt via dediziertem Knopf zu senden).
* Sprach-und-Video-Anrufe (Voraussetzung ist aktives https).

Disclaimer: Damit das Chatfenster angezeigt wird, muss dein Gegner den Web-Caller geöffnet haben. Darüberhinaus ist ein Chat mit mehreren Spielern aktuell (noch) nicht möglich (ausschließlich im 1v1, Spielvariante: X01)

#### Calling

* Audio-Wiedergabe direkt über einen Browser deiner Wahl (das aktuelle voice-pack wird einmalig heruntergeladen bzw. aktualisiert und dann, um eine unverzögerte Wiedergabe zu ermöglichen, im cache abgespeichert).
* Anzeige des aktuellen Sprechers (voice-pack).
* Auswahlmenü zum Wechseln auf einen bestimmmten Sprecher.
* Knopf zum Wechseln auf einen anderen zufälligen Sprecher.
* Auswahlmenüs zur Anpassung von Sprache und Geschlecht.
* Knopf zum Bannen des aktuellen Sprechers.
* Mod-Bereich für zufallsbasierte Stimmen-Anpassung.

Disclaimer: For a continuous calling experience on mobile devices, make sure your device display stays on while you are playing.

#### Board

* Knopf zum automatischen Kalibrieren deines Boards
* Knopf zum Zurücksetzen deines Boards

#### Game

* "Magic-Knopf" zum automatischen "Weiterschalten" von Lobby, Aufnahme und Spiel (je nachdem, welchen Status das aktuelle Match gerade aufweist.)








### Sound-file-keys

***EVERY SOUND-FILE NEEDS TO BE .mp3 or .wav***

**MAIN:**

- gameon
- matchon
- gameshot
- matchshot
- matchcancel
- bulling_start
- bulling_end
- leg_{x}
- set_{x}
- busted
- 0-180
- {playername} (-CCP > 0)
- you_require (-PCC = 1 and -PCCSF = 0)
- yr_2-yr_170 (-PCC = 1 and -PCCSF = 1)

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
- lobby_ambient_in
- lobby_ambient_out

**LOBBY**

- {playername}
- average
- 0-180
- left

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
- -R / --random_caller [Default: 1] [Possible values: 0 | 1]
- -RL / --random_caller_language [Default: 1] [Possible values: look at description below]
- -RG / --random_caller_gender [Default: 0] [Possible values: look at description below]
- -CCP / --call_current_player [Default: 1] [Possible values: 0 | 1]
- -E / --call_every_dart [Default: 0] [Possible values: 0 | 1 | 2]
- -PCC / --possible_checkout_call [Default: 1] [Possible values: 0..Inf]
- -PCCSF / --possible_checkout_call_single_files [Default: 1] [Possible values: 0 | 1]
- -PCCYO / --possible_checkout_call_yourself_only [Default: 0] [Possible values: 0 | 1]
- -A / --ambient_sounds [Default: 0.0] [Possible values: 0.0 .. 1.0]
- -AAC / --ambient_sounds_after_calls [Default: 0] [Possible values: 0 | 1]
- -DL / --downloads [Default: 1] [Possible values: 0 | 1]
- -DLL / --downloads_limit [Default: 3]
- -DLLA / --downloads_language [Default: 1] [Possible values: look at description below]
- -DLN / --downloads_name [Default: '']
- -BLP / --blacklist_path [Default: '']
- -BAV / --background_audio_volume [Default: 0.0] [Possible values: 0.0 .. 1.0]
- -LPB / --local_playback [Default: 1] [Possible values: 0 | 1]
- -WEBDH / --web_caller_disable_https [Default: 0] [Possible values: 0 | 1]
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

Sets a specific voice-pack as caller. On start the application displays a list of installed voice-packs; copy the name of chosen one and paste it here. By default this is 'None' meaning the application chooses a random caller (voice-pack).

*`-R / --random_caller`*

The application will randomly choose a voice-pack. If you use this functionality, the application only considers most recent version of a voice-pack by finding its highest version number by name. Example: 'en-US-Joey-Male-v3'. Because there is no voice-pack with name 'en-US-Joey-Male-v4', version is 'v3' (en-US-Joey-Male-v3). By default this is '1'.

- '0' = random caller deactivated (instead use -C to set your favorite caller)
- '1' = random caller for every match-start
- '2' = random caller for every leg

*`-RL / --random_caller_language`*

Filters randomly chosen voice-pack by its language. '0' means no filtering (every language). By default this is '1' (english).

- '0' = every language
- '1' = english
- '2' = french
- '3' = russian
- '4' = german
- '5' = spanish
- '6' = dutch

*`-RG / --random_caller_gender`*

Filters randomly chosen voice-pack by its gender. '0' means no filtering (every gender). By default this is '0'.

- '0' = every gender
- '1' = female
- '2' = male

*`-CCP / --call_current_player`*

The application will call playernames for certain events like "you require", "leg/set start", "leg/set end". By default this is activated.

- '0' = call current playername deactivated
- '1' = call current playername activated
- '2' = call current playername also on every playerchange

*`-E / --call_every_dart`*

The application will call every thrown dart. By default this is not activated.

- '0' = call every dart deactivated
- '1' = call every dart by calculating the multiplication of field value and multiplier (for example: you hit a triple 20, resulting in calling 60). If activated the endscore (of 3 darts won't be called)
- '2' = call every dart by calling sound-effects you setup. s1, d1, t1 to s20, d20, t30, outside, sbull, bull. If particular sound-file-key can't be found, it will fallback to common field-name: singleinner, singleouter, single, double, triple.

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
By default this is activated.

*`-DLL / --downloads_limit`*

If you want to limit download-count, you can set it to x most recent. By default this is '3'.

*`-DLLA / --downloads_language`*

If you want to filter downloads for a specific language. '0' means no language-filtering (every language). By default this is '1' (english).

- '0' = every language
- '1' = english
- '2' = french
- '3' = russian
- '4' = german
- '5' = spanish
- '6' = dutch

*`-DLN / --downloads_name`*

If you want to filter downloads to a specific voice-pack-name. '' means no name-filtering. By default this is ''.
For example you could set a value 'en-US-Joey-Male'.

*`-BLP / --blacklist_path`*

The blacklist-file stores voice-pack-names that are undesired for downloads or calls. In other words: those ones are just ignored by the application. To use blacklist define an absolute path where the blacklist-file should be located (it will be generated automatically on application start). You can simply add an undesired voice-pack-name (have a look at available ones on application start) to the file or use the web-caller (press 'Ban Caller'). 

*`-BAV / --background_audio_volume`*

You can not hear any calls as your music is way too loud? Try to set this to '0.03' and let the calls begin :) Default is '0.0' (no background-audio-muting). Note: Only availble for windows-os and local playback (LPB = 1).

*`LPB / --local_playback`*

If you set this to '1' the application will playback audio by using your local speakers.
By default this is activated.

*`-WEBDH / --web_caller_disable_https`*

If you set this to '1' the application will run all connection services with insecure http/ws protocol. It's NOT recommended! 
Also you won't be able to use video-/voice-calls on web-caller.
By default this is not activated.

*`-HP / --host_port`*

The application provides a websocket-service. Other extensions like autodarts-extern or autodarts-wled can connect to this service (wss://ip:port).
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
If you rename any of your sound-files while the application is running you need to restart the application, change the current caller with web-caller or wait until a new match starts (assumed random-caller-functionality (-R) is activated.)

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
- Option 4) put the name of the current caller (voice-pack) in autodarts-caller-banned.txt manually.

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