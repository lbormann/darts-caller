## 2.19.12
- Adding logger for websocket messages to debug disconnects (-MLA)

## 2.19.10
- implement debug messages because of match close issues

## 2.19.10
- Deactivated the matches API endpoint; this endpoint is no longer available for client use

## 2.19.9
- stats backend update

## 2.19.8
- Improved Blind Support busted announcments
  - just play a fixed busted sound to not confuse the blind player with different calls like "thrown to high"

## 2.19.6
- Improved Blind Support "you require" announcements
  - Now uses specific sound variant you_require+1.mp3 for consistent tone
  - Skips "you require" announcement when dart scores zero (miss/outside)
- Added play_sound_effect_variant() function
  - Allows playing specific sound file variants (e.g., filename+1.mp3)
  - Falls back to random selection if variant not found

## 2.19.5
- Fixed Blind Support duplicate score announcements
  - Total score now announced only once after 3rd dart
  - Removed duplicate announcement after "Turn ended"
  - Bot total scores now announced correctly
- Fixed Blind Support dart position announcement order
  - Dart position now announced BEFORE "you require" in checkout range
  - Proper sequence: Position → "you require X" (darts 1-2), Position only (dart 3)
- Blind Support now works independently of CALL_EVERY_DART setting
  - No longer requires -E parameter to function

## 2.19.4
- Added Blind Support feature (-CBS / --call_blind_support)
  - Announces target field at the start of each player's turn (for applicable game modes)
  - Announces exact dart position after every throw with intelligent sound file usage
  - Supported game modes: X01, ATC, RTW, Bermuda, Shanghai, Count-Up, Gotcha
  - Replaces normal game mode calls when enabled to prevent duplicates
  - Smart dart position announcements:
    - Outer Single: Only number (e.g., "20")
    - Inner Single: "inside" + number (e.g., "inside 20")
    - Triple: Uses t-prefix files (e.g., "t20") with fallback to "triple 20"
    - Double: Uses d-prefix files (e.g., "d20") with fallback to "double 20"
    - Outside: Uses m-prefix files (e.g., "m20") with fallback to "outside 20"
    - Bull/Bullseye: Direct announcement
  - Corrected Bermuda rounds mapping (12-13-14-D-15-16-17-T-18-19-20-25-50)
  - Required sound files: bs_target_is, bs_single_inner, bs_any_double, bs_any_triple, plus existing t*, d*, m* files
    - the soundfiles are included in new pack versions for all googleai and openai voices. 

## 2.19.3
- Added CustomArgumentParser class for improved error output on invalid arguments
  - Shows only relevant error messages instead of full help text
  - Provides helpful hints based on error type

## 2.19.2
- stability update and debug posibilitys

## 2.19.1
- reactivate possibility to use the Caller standalone via source
- changed webcaller design
- add new soundpacks
- add new languages IT, RU
- add more realistic caller behaviour arg -CRL "--caller-real-life" (just X01)
- add if no playername soundkey avaialble play "player one, two....." 

## 2.18.6
- implementet more detailes user Stats to debug faster
    - no personal data will be stored
- prepare for new soundpacks and languages
    - new variable voices
    - RU, IT will come in the future

## 2.18.5
- add messages for Debug Stop Listening during the match
- implement Broadcast messages for new Extension Darts-Stats
- change client secret and ID implementation
- Bugfix Board IP
- Bugfix WS Message failed
- USER NEED TO UPDATE TO GET CALLER RUNNING IN THE FUTURE

## 2.17.13
- Bugfix playercolors Turnament mode
- Bugfix Random Checkout


## 2.17.11
- forward Player Index to extensions
    - Useable for Player Colors in WLED extension. WLED update required.

## 2.17.10
- Implement Tactics


## 2.17.8
- Bermuda: if you dont hit target, Broadcast Busted for extensions

## 2.17.6
- Soundfile Updates and Hoster change
- Gotscha Bugfix


## 2.17.4
 - Count Up implemented
 - Bermuda implemented (Soundfile for minus score required | minus.mp3)
 - Shanghai implemented
 - Gotcha implemented (Soundfile for opponend score reset required | score_denied.mp3)
 - bugfix

## 2.16.2
 - bugfix

## 2.16.1
 - adds user stats

## 2.16.0
 - implement single dart broadcast when call every dart 1

## 2.15.0
 - implement board status messages for wled (Takeout Status, Calibration, Board start/stop....)
 - implement match-end broadcast for wled off parameter

## 2.14.0

- add argument -ROVP --remove_old_voice_packs (default '0')
- add argument -CBA --call_bot_actions (default '1')
- extend argument -E (The former E = 2 is now E = 3. The "new E = 2" calls a single dart by its field-name / category "SINGLE-DART-NAME")
- rename sound-file-keys of category "SINGLE-DART-EFFECT": add prefix "effects_" to every sound-file-key. Examples: 't20' is now 'effect_t20', 'single' is now 'effect_single' (You need to rename your files accordingly)
- rename sound-file-key 'sbull' to 'effect_bull' (You need to rename your file accordingly)
- rename sound-file-key 'bull' to 'effect_bullseye' (You need to rename your file accordingly)
- add sound-file-key 'ambient_matchcancel'
- fix bug where checkout-counter wasn't reset properly
- update all existing amazon/aws voice-packs (containing sounds for "E = 2")
- rearrange preference-buttons on web-caller
- adjust README to changes


## 2.13.0

- rename application to darts-caller
- fix gender selection when selected language is not 'every language'


## 2.12.5

- simplify README (argument section)
- remove argument -DLL (it is now covered by -DL)
- remove argument -PCCSF (from now it will automatically fallback to "single-files" when sound-file-key 'you_require' is not available)
- add sound-file-keys for particular checkout-numbers: 'c_2-c_170'
- add sound-file-keys for particular bogey-numbers: 'ambient_bogey_number_{bogey_number}'


## 2.12.4

- change sound-file-key 'lobby_ambient_in' to 'ambient_lobby_in'
- change sound-file-key 'lobby_ambient_out' to 'ambient_lobby_out'
- remove argument -BLP
- add caller fav mechanismn
- fix bug for option -C
- reposition inputs on web-caller (for better practical use)


## 2.12.3

- improve change-caller speed
- fix bug for change-caller
- improve "magic-next-button" for bulling


## 2.12.2

- fix sound-file-keys sbull, bull


## 2.12.1

- fix bug on caller-setup
- add argument -ETS (call_every_dart_total_score)


## 2.12.0

- add direct voice-pack selection to web-caller
- add "magic next button" to web-caller
- add option -E to web-caller
- add option -CCP to web-caller
- add option -PCC to web-caller
- add option -PCCYO to web-caller
- add voice-pack 'en-GB-Amy-Female'
- add voice-pack 'en-GB-Arthur-Male'
- add voice-pack 'es-ES-Lucia-Female'
- add voice-pack 'es-ES-Sergio-Male'
- add voice-pack 'fr-FR-Remi-Male'
- add voice-pack 'fr-FR-Lea-Female'
- update all existing amazon/aws voice-packs
- remove all google-cloud-tts voice-packs (*-wavenet-*)
- remove web-scoreboard
- remove arguments -WEB, -WEBSB, -WEBP, -L, -CCPA, -ESF
- rework argument -E (call_every_dart)
- rework argument -R (random_caller)
- rework argument -CCP (call_current_player)
- add argument -LPB (local_playback) => playbacks audio locally / default: yes
- support argument -C (caller) without specification of voice-pack-version
- add sound-file-key 'ambient_playerchange_{playername}
- support blacklisting without specific voice-pack-version
- rework websockets (fix browser incompatibilities and improve ios device support)
- process token-refresh response correctly
- rework README


## 2.11.1

- improve RTW
- treat connection loss for kc
- add board-functions to web-caller


## 2.11.0

- add voice-/video-calls to match-chat
- add support RTW (Round the world)
- rework lobby sounds


## 2.10.3

- improve chat UX
- add chat settings (DC-id/username)
- add chat link functionality
- update all amazon/aws voice-packs


## 2.10.2

- add image-transfer to match-chat
- fix bugs match-chat


## 2.10.1

- fix connection-bug on match-chat


## 2.10.0

- add realtime p2p-match-chat to web-caller


## 2.9.0

- add language and gender selection to web-caller
- add voice-pack 'en-US-Justin-Male'


## 2.8.12

- add voice-pack 'nl-NL-Laura-Female'
- add voice-pack 'de-AT-Hannah-Female'


## 2.8.11

- update voice-pack 'de-DE-Daniel-Male'
- update voice-pack 'en-US-Joey-Male'
- update voice-pack 'en-US-Joanna-Female'
- update voice-pack 'en-US-Matthew-Male'
- update voice-pack 'en-US-Danielle-Female'


## 2.8.10

- fix call-repetitions


## 2.8.9

- add bull-off-calling


## 2.8.8

- add lobby-event broadcasts
- improve custom-event`s data structure
- update voice-pack 'de-DE-Vicki-Female'
- update voice-pack 'en-US-Gregory-Male'


## 2.8.7

- fix blacklist-file-creation
- update voice-pack 'en-US-Kendra-Female'


## 2.8.6

- fix web-host


## 2.8.5

- fix web-caller queue


## 2.8.4

- rework path-validation
- add voice-pack 'en-US-Kevin-Male'
- add voice-pack 'en-US-Salli-Female'
- fix reconnect-loop for chrome android
- fix left lobby-sounds


## 2.8.3

- add "say-something" to web-caller
- add volume-mod to web-caller
- add randomizer-mod to web-caller
- add voice-pack 'en-US-Ruth-Female'


## 2.8.2

- improved web-callers`s sync-performance by factor 3 to 5
- fix coords for field 14


## 2.8.1

- improve sound-mods: prevent extreme differences in associated sounds
- correct every sound-event for mod-ability
- add sound-file-key for bogey numbers (ambient_bogey_number)


## 2.8.0

- prevent app from start twice
- add sound-mods to web-caller: choose ranges for random playback-rate and detune
- fix error that crashes web-calling
- remove ban/change for web-caller if not available
- add voice-packs 'en-US-Danielle-Female' and 'en-US-Kimberly-Female'


## 2.7.5

- hotfix: disables: prevent app from start twice


## 2.7.4

- improve web-caller (load all files on start + "change/ban-caller"-function)
- add voice-pack 'en-US-Matthew-Male'
- preview banned voice-packs
- add fallback for unreachable audio device
- prevent app from start twice


## 2.7.3

- hotfix: fix typo


## 2.7.2

- hotfix: fix occasional call-stops after one match
- change file-hoster for more stable downloads
- add option for downloads: only download specific voice-pack by its name
- add ambient_gameshot_{playername}, ambient_matchshot_{playername} and more
- add voice-pack 'en-US-Gregory-Male'


## 2.7.1

- hotfix: receive_local_board_address


## 2.7.0

- extend lobby-calling (lobbychanged -> lobby_ambient_in)
- improve web-caller (using indexeddb for caching to continously prevent delays)
- change file-hoster for more stable downloads (dropbox)
- update voice-packs (new lobby-sounds, 2000+ new playernames)
- add path argument for blacklist-file
- fix token-requests
- fix empty-SHARED_MEDIA_PATH error


## 2.6.3

- add CHANGELOG
- add BACKLOG
- fix possible invalid path configuration for linux/macos
- reintroduce "lobbychanged" sound-file-key
- introduce support for game-variant "ATC" (Around-the-clock); thanks to @takki2602 
- improve -M / -DL description
- CALL_CURRENT_PLAYER_ALWAYS only with more than one player


## 0.0.0

- prevent from double calling
- only one webhook with all information (to prevent race condition on receiving app): leg_end, turn, throw_number, throw_value, points_left, variant, user
- let the user configure caller-volume
- sounds for every throw (single, double, tripple, missed)
- add start argument for surpressing checkout calls
- add sites for free sound-file downloads
- cricket: Change call behaviour to default
- improved possible checkout call for bogey numbers
- yr_2-yr_170.{wav | mp3} different sounds-files for possible checkout calls
- fix sound-play repetition
- improved error logging
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
- add debug by argument
- add caller-profile-downloader
- add media_path_shared
- fix sending to websocket take too long / waiting for sound-playing (rework process_*)
- optional activation of third dart (-E)
- add "ambient1More"
- add Readme-section for updating
- background-audio-muting for windows-os
- keys for dart-number-combinations ie ambient_t1d1s1 -> sound
- add linux start-script
- start board on app-start if board-address is available!
- dl limit remove 1000 cap
- consider x.leg/set -> Gameshot / !x_leg! / player
- add ambient_group_level
- prohibit -M and -MS in main-directory; prohibit -MS in -M
- https://discord.com/channels/802528604067201055/955745166134747196/1089977962725650603
- add web-caller
- configure custom web-caller-port
- added caller language and gender filter
- fixed random-caller and random-caller-each-leg
- adds PCCYO
- rework PCC
- add support for game control
- add support for gc: dart-correction (multiple)
- add ban/change caller
