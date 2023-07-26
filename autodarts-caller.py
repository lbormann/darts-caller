import os
from pathlib import Path
import time
import json
import platform
import random
import argparse
from keycloak import KeycloakOpenID
import requests
from pygame import mixer
import websocket
import socket
from websocket_server import WebsocketServer
import threading
import logging
from download import download
import shutil
import csv
import math
import ssl
import sys
from urllib.parse import quote, unquote
from flask import Flask, render_template, send_from_directory

plat = platform.system()
if plat == 'Windows':
    from pycaw.pycaw import AudioUtilities


sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
sh.setFormatter(formatter)
logger=logging.getLogger()
logger.handlers.clear()
logger.setLevel(logging.INFO)
logger.addHandler(sh)

app = Flask(__name__)
main_directory = os.path.dirname(os.path.realpath(__file__))







VERSION = '2.2.8'

DEFAULT_HOST_IP = '0.0.0.0'
DEFAULT_HOST_PORT = 8079
DEFAULT_CALLER = None
DEFAULT_DOWNLOADS = True
DEFAULT_WEB_CALLER_PORT = 5000

DEFAULT_DOWNLOADS_LIMIT = 0
DEFAULT_DOWNLOADS_PATH = 'caller-downloads-temp'
DEFAULT_EMPTY_PATH = ''
DEFAULT_MIXER_FREQUENCY = 44100
DEFAULT_MIXER_SIZE = 32
DEFAULT_MIXER_CHANNELS = 2
DEFAULT_MIXER_BUFFERSIZE = 4096

AUTODART_URL = 'https://autodarts.io'
AUTODART_AUTH_URL = 'https://login.autodarts.io/'
AUTODART_AUTH_TICKET_URL = 'https://api.autodarts.io/ms/v0/ticket'
AUTODART_CLIENT_ID = 'autodarts-app'
AUTODART_REALM_NAME = 'autodarts'
AUTODART_MATCHES_URL = 'https://api.autodarts.io/gs/v0/matches/'
AUTODART_BOARDS_URL = 'https://api.autodarts.io/bs/v0/boards/'
AUTODART_WEBSOCKET_URL = 'wss://api.autodarts.io/ms/v0/subscribe?ticket='

SUPPORTED_SOUND_FORMATS = ['.mp3', '.wav']
SUPPORTED_GAME_VARIANTS = ['X01', 'Cricket', 'Random Checkout']
SUPPORTED_CRICKET_FIELDS = [15, 16, 17, 18, 19, 20, 25]
BOGEY_NUMBERS = [169, 168, 166, 165, 163, 162, 159]


CALLER_PROFILES = {
    # C7
    'charles-m-english-us-canada': 'https://drive.google.com/file/d/1-CrWSFHBoT_I9kzDuo7PR7FLCfEO-Qg-/view?usp=sharing',
    'clint-m-english-us-canada': 'https://drive.google.com/file/d/1-IQ9Bvp1i0jG6Bu9fMWhlbyAj9SkoVGb/view?usp=sharing',
    'alicia-f-english-us-canada': 'https://drive.google.com/file/d/1-Cvk-IczRjOphDOCA14NwE1hy4DAB8Tt/view?usp=sharing',
    'kushal-m-english-india': 'https://drive.google.com/file/d/1-GavAG_oa3MrrremanvfYSfMI0U784EN/view?usp=sharing',
    'kylie-f-english-australia': 'https://drive.google.com/file/d/1-Y6XpdFjOotSLBi0sInf5CGpAAV3mv0b/view?usp=sharing',
    'ruby-f-english-uk': 'https://drive.google.com/file/d/1-kqVwCd4HJes0EVNda5EOF6tTwUxql3z/view?usp=sharing',
    'ethan-m-english-us-canada': 'https://drive.google.com/file/d/106PG96DLzcHHusbQ2zRfub2ZVXbz5TPs/view?usp=sharing',
    'mitch-m-english-australia': 'https://drive.google.com/file/d/10XEf0okustuoHnu2h_4eqRA6G-2d2mH1/view?usp=sharing',
    'ava-f-english-us-canada': 'https://drive.google.com/file/d/10XtdjfORUreALkcUxbDhjb0Bo6ym7IDK/view?usp=sharing',
    'aiden-m-english-uk': 'https://drive.google.com/file/d/10bYvcqp1nzqJnBDC7B6u7s8aequ5wGat/view?usp=sharing',
    'theo-m-english-uk': 'https://drive.google.com/file/d/10eQaYMZM3tkIA2PIDsb0r-5NhyDU86-C/view?usp=sharing',
    'emily-f-english-scottish': 'https://drive.google.com/file/d/10mOzTjA5tqBZCKI3EqxJ0YvQptqtMNQg/view?usp=sharing',
}



def ppi(message, info_object = None, prefix = '\r\n'):
    logger.info(prefix + str(message))
    if info_object != None:
        logger.info(str(info_object))
    
def ppe(message, error_object):
    ppi(message)
    if DEBUG:
        logger.exception("\r\n" + str(error_object))


def get_local_ip_address(target='8.8.8.8'):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((target, 80))
        ip_address = s.getsockname()[0]
        s.close()
    except:
        ip_address = DEFAULT_HOST_IP
    return ip_address

def download_callers(): 
    if DOWNLOADS:
        download_list = CALLER_PROFILES
        if DOWNLOADS_LIMIT > 0:
            download_list = {k: CALLER_PROFILES[k] for k in list(CALLER_PROFILES.keys())[-DOWNLOADS_LIMIT:]}

        if len(download_list) > 0:
            if os.path.exists(AUDIO_MEDIA_PATH) == False: os.mkdir(AUDIO_MEDIA_PATH)

        # Download and parse every caller-profile
        for cpr_name, cpr_download_url in download_list.items():
            try:
                # Check if caller-profile already present in users media-directory, yes ? -> stop for this caller-profile
                caller_profile_exists = os.path.exists(os.path.join(AUDIO_MEDIA_PATH, cpr_name))
                if caller_profile_exists == True:
                    # ppi('Caller-profile ' + cpr_name + ' already exists -> Skipping download')
                    continue

                # clean download-area!
                shutil.rmtree(DOWNLOADS_PATH, ignore_errors=True)
                if os.path.exists(DOWNLOADS_PATH) == False: 
                    os.mkdir(DOWNLOADS_PATH)
                
                # Download caller-profile and extract archive
                dest = os.path.join(DOWNLOADS_PATH, 'download.zip')

                # kind="zip", 
                path = download(cpr_download_url, dest, progressbar=True, replace=False, verbose=DEBUG)
 
                # TEMP Test!!
                # shutil.copyfile('C:\\Users\\Luca\\Desktop\\WORK\\charles-m-english-us-canada\\download.zip', os.path.join(DOWNLOADS_PATH, 'download.zip'))

                shutil.unpack_archive(dest, DOWNLOADS_PATH)
                os.remove(dest)
        
                # Find sound-file-archive und extract it
                zip_filename = [f for f in os.listdir(DOWNLOADS_PATH) if f.endswith('.zip')][0]
                dest = os.path.join(DOWNLOADS_PATH, zip_filename)
                shutil.unpack_archive(dest, DOWNLOADS_PATH)
                os.remove(dest)

                # Find folder and rename it to properly
                sound_folder = [dirs for root, dirs, files in sorted(os.walk(DOWNLOADS_PATH))][0][0]
                src = os.path.join(DOWNLOADS_PATH, sound_folder)
                dest = os.path.splitext(dest)[0]
                os.rename(src, dest)

                # Find template-file and parse it
                template_file = [f for f in os.listdir(DOWNLOADS_PATH) if f.endswith('.csv')][0]
                template_file = os.path.join(DOWNLOADS_PATH, template_file)
                san_list = list()
                with open(template_file, 'r', encoding='utf-8') as f:
                    tts = list(csv.reader(f, delimiter=';'))
                    for event in tts:
                        sanitized = list(filter(None, event))
                        if len(sanitized) == 1:
                            sanitized.append(sanitized[0].lower())
                        san_list.append(sanitized)
                    # ppi(san_list)

                # Find origin-file
                origin_file = None
                files = [f for f in os.listdir(DOWNLOADS_PATH) if f.endswith('.txt')]
                if len(files) >= 1:
                    origin_file = os.path.join(DOWNLOADS_PATH, files[0])

                # Move template- and origin-file to sound-dir
                if origin_file != None:
                    shutil.move(origin_file, dest)
                shutil.move(template_file, dest)   

                # Find all supported sound-files and remember names 
                sounds = []
                for root, dirs, files in os.walk(dest):
                    for file in sorted(files):
                        if file.endswith(tuple(SUPPORTED_SOUND_FORMATS)):
                            sounds.append(os.path.join(root, file))
                # ppi(sounds)

                # Rename sound-files and copy files according the defined caller-keys
                for i in range(len(san_list) - 1):
                    current_sound = sounds[i]
                    current_sound_splitted = os.path.splitext(current_sound)
                    current_sound_extension = current_sound_splitted[1]

                    try:
                        row = san_list[i]
                        caller_keys = row[1:]
                        # ppi(caller_keys)

                        for ck in caller_keys:
                            multiple_file_name = os.path.join(dest, ck + current_sound_extension)
                            exists = os.path.exists(multiple_file_name)
                            # ppi('Test existance: ' + multiple_file_name)

                            counter = 0
                            while exists == True:
                                counter = counter + 1
                                multiple_file_name = os.path.join(dest, ck + '+' + str(counter) + current_sound_extension)
                                exists = os.path.exists(multiple_file_name)
                                # ppi('Test (' + str(counter) + ') existance: ' + multiple_file_name)

                            shutil.copyfile(current_sound, multiple_file_name)
                    except Exception as ie:
                        ppe('Failed to process entry "' + row[0] + '"', ie)
                    finally:
                        os.remove(current_sound)

                shutil.move(dest, AUDIO_MEDIA_PATH)
                ppi('A new caller was added: ' + cpr_name)

            except Exception as e:
                ppe('Failed to process caller-profile: ' + cpr_name, e)
            finally:
                shutil.rmtree(DOWNLOADS_PATH, ignore_errors=True)

def load_callers():
    # load shared-sounds
    shared_sounds = {}
    if AUDIO_MEDIA_PATH_SHARED != DEFAULT_EMPTY_PATH: 
        for root, dirs, files in os.walk(AUDIO_MEDIA_PATH_SHARED):
            for filename in files:
                if filename.endswith(tuple(SUPPORTED_SOUND_FORMATS)):
                    full_path = os.path.join(root, filename)
                    base = os.path.splitext(filename)[0]
                    key = base.split('+', 1)[0]
                    if key in shared_sounds:
                        shared_sounds[key].append(full_path)
                    else:
                        shared_sounds[key] = [full_path]

    # load callers
    callers = []
    for root, dirs, files in os.walk(AUDIO_MEDIA_PATH):
        file_dict = {}
        for filename in files:
            if filename.endswith(tuple(SUPPORTED_SOUND_FORMATS)):
                full_path = os.path.join(root, filename)
                base = os.path.splitext(filename)[0]
                key = base.split('+', 1)[0]
                if key in file_dict:
                    file_dict[key].append(full_path)
                else:
                    file_dict[key] = [full_path]
        if file_dict:
            callers.append((root, file_dict))
        
    # add shared-sounds to callers
    for ss_k, ss_v in shared_sounds.items():
        for (root, c_keys) in callers:
            if ss_k in c_keys:
                # for sound_variant in ss_v:
                #     c_keys[ss_k].append(sound_variant)
                if CALL_EVERY_DART == True and CALL_EVERY_DART_SINGLE_FILE == True:
                    c_keys[ss_k] = ss_v
                else:
                    for sound_variant in ss_v:
                        c_keys[ss_k].append(sound_variant)
            else:
                c_keys[ss_k] = ss_v


    

    return callers

def setup_caller():
    global caller
    caller = None

    callers = load_callers()
    ppi(str(len(callers)) + ' caller(s) ready to call out your Darts:')

    if CALLER != DEFAULT_CALLER and CALLER != '':
        wished_caller = CALLER.lower()
        for c in callers:
            caller_name = os.path.basename(os.path.normpath(c[0])).lower()
            ppi(caller_name, None, '')
            if caller == None and caller_name == wished_caller:
                caller = c

    else:
        for c in callers: 
            caller_name = os.path.basename(os.path.normpath(c[0])).lower()
            ppi(caller_name, None, '')

        if RANDOM_CALLER == False:
            caller = callers[0]
        else:
            caller = random.choice(callers)

    if(caller != None):
        for sound_file_key, sound_file_values in caller[1].items():
            sound_list = list()
            for sound_file_path in sound_file_values:
                sound_list.append(sound_file_path)
            caller[1][sound_file_key] = sound_list

        ppi("Your current caller: " + str(os.path.basename(os.path.normpath(caller[0]))) + " knows " + str(len(caller[1].values())) + " Sound-file-key(s)")
        # ppi(caller[1])
        caller = caller[1]

def receive_local_board_address():
    try:
        global accessToken
        global boardManagerAddress

        if boardManagerAddress == None:
            res = requests.get(AUTODART_BOARDS_URL + AUTODART_USER_BOARD_ID, headers={'Authorization': 'Bearer ' + accessToken})
            board_ip = res.json()['ip']
            if board_ip != None and board_ip != '':  
                boardManagerAddress = 'http://' + board_ip
                ppi('Board-address: ' + boardManagerAddress) 
            else:
                boardManagerAddress = None
                ppi('Board-address: UNKNOWN') 
            
    except Exception as e:
        boardManagerAddress = None
        ppe('Fetching local-board-address failed', e)

def play_sound(sound, wait_for_last, volume_mult):
    if WEB > 0:
        mirror = {
                "event": "mirror",
                "file": quote(sound, safe=""),
                "wait": wait_for_last
            }
        broadcast(mirror)

    if WEB == 0 or WEB == 2:
        if wait_for_last == True:
            while mixer.get_busy():
                time.sleep(0.01)

        s = mixer.Sound(sound)
        if AUDIO_CALLER_VOLUME is not None:
            s.set_volume(AUDIO_CALLER_VOLUME * volume_mult)
        s.play()

    ppi('Playing: "' + sound + '"')

def play_sound_effect(sound_file_key, wait_for_last = False, volume_mult = 1.0):
    try:
        global caller
        play_sound(random.choice(caller[sound_file_key]), wait_for_last, volume_mult)
        
        return True
    except Exception as e:
        ppe('Can not play sound for sound-file-key "' + sound_file_key + '" -> Ignore this or check existance; otherwise convert your file appropriate', e)
        return False


def listen_to_newest_match(m, ws):
    global currentMatch

    # EXAMPLE
    # {
    #     "channel": "autodarts.boards",
    #     "data": {
    #         "event": "start",
    #         "id": "82f917d0-0308-2c27-c4e9-f53ef2e98ad2"
    #     },
    #     "topic": "1ba2df53-9a04-51bc-9a5f-667b2c5f315f.matches"  
    # }

    if m['event'] == 'start':
        currentMatch = m['id']
        ppi('Listen to match: ' + currentMatch)

        try:
            global accessToken
            res = requests.get(AUTODART_MATCHES_URL + currentMatch, headers={'Authorization': 'Bearer ' + accessToken})
            m = res.json()
            mode = m['variant']

            # ppi(json.dumps(m, indent = 4, sort_keys = True))

            if mode == 'X01':
                # Determine "baseScore"-Key
                base = 'baseScore'
                if 'target' in m['settings']:
                    base = 'target'

                matchStarted = {
                    "event": "match-started",
                    "player": m['players'][0]['name'],
                    "game": {
                        "mode": mode,
                        "pointsStart": str(m['settings'][base]),
                        # TODO: fix
                        "special": "TODO"
                        }     
                    }
                broadcast(matchStarted)

            elif mode == 'Cricket':
                matchStarted = {
                    "event": "match-started",
                    "player": m['players'][0]['name'],
                    "game": {
                        "mode": mode,
                        # TODO: fix
                        "special": "TODO"
                        }     
                    }
                broadcast(matchStarted)


            callPlayerNameState = play_sound_effect(m['players'][0]['name'])
            if play_sound_effect('matchon', callPlayerNameState) == False:
                play_sound_effect('gameon', callPlayerNameState)

            if AMBIENT_SOUNDS != 0.0 and play_sound_effect('ambient_matchon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS) == False:
                play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)

            ppi('Matchon')

        except Exception as e:
            ppe('Fetching initial match-data failed', e)

        global isGameFinished
        isGameFinished = False

        receive_local_board_address()
        # if boardManagerAddress != None:
        #     res = requests.post(boardManagerAddress + '/api/reset')
        #     time.sleep(0.25)
        #     res = requests.put(boardManagerAddress + '/api/start')

        paramsSubscribeMatchesEvents = {
            "channel": "autodarts.matches",
            "type": "subscribe",
            "topic": currentMatch + ".state"
        }

        ws.send(json.dumps(paramsSubscribeMatchesEvents))
        
    elif m['event'] == 'finish' or m['event'] == 'delete':
        ppi('Stop listening to match: ' + m['id'])

        paramsUnsubscribeMatchEvents = {
            "type": "unsubscribe",
            "channel": "autodarts.matches",
            "topic": m['id'] + ".state"
        }
        ws.send(json.dumps(paramsUnsubscribeMatchEvents))

        if m['event'] == 'delete':
            play_sound_effect('matchcancel')

def process_match_x01(m):
    global accessToken
    global currentMatch
    global isGameFinished
    global lastPoints

    variant = m['variant']
    currentPlayerIndex = m['player']
    currentPlayer = m['players'][currentPlayerIndex]
    currentPlayerName = str(currentPlayer['name']).lower()
    remainingPlayerScore = m['gameScores'][currentPlayerIndex]

    turns = m['turns'][0]
    points = str(turns['points'])
    busted = (turns['busted'] == True)
    matchshot = (m['winner'] != -1 and isGameFinished == False)
    gameshot = (m['gameWinner'] != -1 and isGameFinished == False)
    
    # Determine "baseScore"-Key
    base = 'baseScore'
    if 'target' in m['settings']:
        base = 'target'
    
    matchon = (m['settings'][base] == m['gameScores'][0] and turns['throws'] == None and m['leg'] == 1 and m['set'] == 1)
    gameon = (m['settings'][base] == m['gameScores'][0] and turns['throws'] == None)

    # ppi('matchon: '+ str(matchon) )
    # ppi('gameon: '+ str(gameon) )
    # ppi('isGameFinished: ' + str(isGameFinished))

    pcc_success = False
    isGameFin = False

    if turns != None and turns['throws'] != None:
        lastPoints = points


    # Darts pulled (Playerchange and Possible-checkout)
    if gameon == False and turns != None and turns['throws'] == None or isGameFinished == True:
        busted = "False"
        if lastPoints == "B":
            lastPoints = "0"
            busted = "True"

        dartsPulled = {
            "event": "darts-pulled",
            "player": currentPlayerName,
            "game": {
                "mode": variant,
                # TODO: fix
                "pointsLeft": str(remainingPlayerScore),
                # TODO: fix
                "dartsThrown": "3",
                "dartsThrownValue": lastPoints,
                "busted": busted
                # TODO: fix
                # "darts": [
                #     {"number": "1", "value": "60"},
                #     {"number": "2", "value": "60"},
            
                #     {"number": "3", "value": "60"}
                # ]
            }
        }
        # ppi(dartsPulled)
        broadcast(dartsPulled)

        if gameon == False and isGameFinished == False:

            # Check for possible checkout
            if POSSIBLE_CHECKOUT_CALL and m['player'] == currentPlayerIndex and remainingPlayerScore <= 170 and remainingPlayerScore not in BOGEY_NUMBERS:
                play_sound_effect(currentPlayerName)

                remaining = str(remainingPlayerScore)

                if POSSIBLE_CHECKOUT_CALL_SINGLE_FILE:
                    pcc_success = play_sound_effect('yr_' + remaining, True)
                    if pcc_success == False:
                        pcc_success = play_sound_effect(remaining, True)
                else:
                    pcc_success = (play_sound_effect('you_require', True) and play_sound_effect(remaining, True))

                ppi('Checkout possible: ' + remaining)

            # Player`s turn-call
            if CALL_CURRENT_PLAYER and m['player'] == currentPlayerIndex and pcc_success == False:
                pcc_success = play_sound_effect(currentPlayerName)

            # Player-change
            if pcc_success == False and AMBIENT_SOUNDS != 0.0:
                play_sound_effect('ambient_playerchange', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)

            ppi("Next player")

    # Call every thrown dart
    elif CALL_EVERY_DART == True and turns != None and turns['throws'] != None and len(turns['throws']) >= 1 and busted == False and matchshot == False and gameshot == False: 

        throwAmount = len(turns['throws'])
        type = turns['throws'][throwAmount - 1]['segment']['bed'].lower()
        field_name = turns['throws'][throwAmount - 1]['segment']['name'].lower()
 
        if field_name == '25':
            field_name = 'sbull'

        # ppi("Type: " + str(type) + " - Field-name: " + str(field_name))

        if CALL_EVERY_DART_SINGLE_FILE == True:
            if play_sound_effect(field_name) == False:
                inner_outer = False
                if type == 'singleouter' or type == 'singleinner':
                    inner_outer = play_sound_effect(type)
                    if inner_outer == False:
                        play_sound_effect('single')
                else:
                    play_sound_effect(type)

        elif len(turns['throws']) <= 2:
            field_number = str(turns['throws'][throwAmount - 1]['segment']['number'])

            if type == 'single' or type == 'singleinner' or type == "singleouter":
                play_sound_effect(field_number)
            elif type == 'double' or type == 'triple':
                play_sound_effect(type)
                play_sound_effect(field_number, True)
            else:
                play_sound_effect('outside')


    # Check for matchshot
    if matchshot == True:
        isGameFin = True
        
        matchWon = {
                "event": "match-won",
                "player": currentPlayerName,
                "game": {
                    "mode": variant,
                    "dartsThrownValue": points
                } 
            }
        broadcast(matchWon)

        if play_sound_effect('matchshot') == False:
            play_sound_effect('gameshot')
    
        play_sound_effect(currentPlayerName, True)

        if play_sound_effect('ambient_matchshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS) == False:
            play_sound_effect('ambient_gameshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)

        setup_caller()
        ppi('Gameshot and match')

    # Check for gameshot
    elif gameshot == True:
        isGameFin = True
        
        gameWon = {
                "event": "game-won",
                "player": currentPlayerName,
                "game": {
                    "mode": variant,
                    "dartsThrownValue": points
                } 
            }
        broadcast(gameWon)

        gameshotState = play_sound_effect('gameshot')

        currentPlayerScoreLegs = m['scores'][currentPlayerIndex]['legs']
        # currentPlayerScoreSets = m['scores'][currentPlayerIndex]['sets']
        currentLeg = m['leg']
        currentSet = m['set']
        maxLeg = m['legs']
        # maxSets = m['sets']

        # ppi('currentLeg: ' + str(currentLeg))
        # ppi('currentSet: ' + str(currentSet))

        if 'sets' not in m:
            play_sound_effect('leg_' + str(currentLeg), gameshotState)
        else:
            if currentPlayerScoreLegs == 0:
                play_sound_effect('set_' + str(currentSet), gameshotState)
            else:
                play_sound_effect('leg_' + str(currentLeg), gameshotState)    

        play_sound_effect(currentPlayerName, True)

        if AMBIENT_SOUNDS != 0.0:
            play_sound_effect('ambient_gameshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)

        ppi('Gameshot')

    # Check for matchon
    elif matchon == True:
        isGameFinished = False

        matchStarted = {
            "event": "match-started",
            "player": currentPlayerName,
            "game": {
                "mode": variant,
                "pointsStart": str(base),
                # TODO: fix
                "special": "TODO"
                }     
            }
        broadcast(matchStarted)

        callPlayerNameState = play_sound_effect(currentPlayerName)
        if play_sound_effect('matchon', callPlayerNameState) == False:
            play_sound_effect('gameon', callPlayerNameState)

        if AMBIENT_SOUNDS != 0.0 and play_sound_effect('ambient_matchon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS) == False:
            play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)

        ppi('Matchon')

    # Check for gameon
    elif gameon == True:
        isGameFinished = False

        gameStarted = {
            "event": "game-started",
            "player": currentPlayerName,
            "game": {
                "mode": variant,
                "pointsStart": str(base),
                # TODO: fix
                "special": "TODO"
                }     
            }
        broadcast(gameStarted)

        callPlayerNameState = play_sound_effect(currentPlayerName)
        play_sound_effect('gameon', callPlayerNameState)

        if AMBIENT_SOUNDS != 0.0:
            play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)

        ppi('Gameon')
          
    # Check for busted turn
    elif busted == True:
        lastPoints = "B"
        isGameFinished = False

        busted = { 
                    "event": "busted",
                    "player": currentPlayerName,
                    "game": {
                        "mode": variant
                    }       
                }
        broadcast(busted)

        play_sound_effect('busted')

        if AMBIENT_SOUNDS != 0.0:
            play_sound_effect('ambient_noscore', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)

        ppi('Busted')
    
    # Check for 1. Dart
    elif turns != None and turns['throws'] != None and len(turns['throws']) == 1:
        isGameFinished = False

    # Check for 2. Dart
    elif turns != None and turns['throws'] != None and len(turns['throws']) == 2:
        isGameFinished = False

    # Check for 3. Dart - Score-call
    elif turns != None and turns['throws'] != None and len(turns['throws']) == 3:
        isGameFinished = False

        dartsThrown = {
            "event": "darts-thrown",
            "player": currentPlayerName,
            "game": {
                "mode": variant,
                "pointsLeft": str(remainingPlayerScore),
                "dartNumber": "3",
                "dartValue": points,        
            }
        }
        broadcast(dartsThrown)

        play_sound_effect(points)

        if AMBIENT_SOUNDS != 0.0:
            ambient_x_success = False

            throw_combo = ''
            for t in turns['throws']:
                throw_combo += t['segment']['name'].lower()
            # ppi(throw_combo)

            if turns['points'] != 0:
                ambient_x_success = play_sound_effect('ambient_' + str(throw_combo), AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)
                if ambient_x_success == False:
                    ambient_x_success = play_sound_effect('ambient_' + str(turns['points']), AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)

            if ambient_x_success == False:
                if turns['points'] >= 150:
                    play_sound_effect('ambient_150more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)   
                elif turns['points'] >= 120:
                    play_sound_effect('ambient_120more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)
                elif turns['points'] >= 100:
                    play_sound_effect('ambient_100more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)
                elif turns['points'] >= 50:
                    play_sound_effect('ambient_50more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)
                elif turns['points'] >= 1:
                    play_sound_effect('ambient_1more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)
                else:
                    play_sound_effect('ambient_noscore', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)


            # Koordinaten der Pfeile
            coords = []
            for t in turns['throws']:
                coords.append({"x": t['coords']['x'], "y": t['coords']['y']})
            # ppi(str(coords))

            # Suche das Koordinatenpaar, das am weitesten von den beiden Anderen entfernt ist

            # Liste mit allen möglichen Kombinationen von Koordinatenpaaren erstellen
            combinations = [(coords[0], coords[1]), (coords[0], coords[2]), (coords[1], coords[2])]

            # Variablen für das ausgewählte Koordinatenpaar und die maximale Gesamtdistanz initialisieren
            selected_coord = None
            max_total_distance = 0

            # Gesamtdistanz für jede Kombination von Koordinatenpaaren berechnen
            for combination in combinations:
                dist1 = math.sqrt((combination[0]["x"] - combination[1]["x"])**2 + (combination[0]["y"] - combination[1]["y"])**2)
                dist2 = math.sqrt((combination[1]["x"] - combination[0]["x"])**2 + (combination[1]["y"] - combination[0]["y"])**2)
                total_distance = dist1 + dist2
                
                # Überprüfen, ob die Gesamtdistanz größer als die bisher größte Gesamtdistanz ist
                if total_distance > max_total_distance:
                    max_total_distance = total_distance
                    selected_coord = combination[0]

            group_score = 100.0
            if selected_coord != None:
                
                # Distanz von selected_coord zu coord2 berechnen
                dist1 = math.sqrt((selected_coord["x"] - coords[1]["x"])**2 + (selected_coord["y"] - coords[1]["y"])**2)

                # Distanz von selected_coord zu coord3 berechnen
                dist2 = math.sqrt((selected_coord["x"] - coords[2]["x"])**2 + (selected_coord["y"] -  coords[2]["y"])**2)

                # Durchschnitt der beiden Distanzen berechnen
                avg_dist = (dist1 + dist2) / 2

                group_score = (1.0 - avg_dist) * 100

            # ppi("Distance by max_dis_coord to coord2: " + str(dist1))
            # ppi("Distance by max_dis_coord to coord3: " + str(dist2))
            # ppi("Group-score: " + str(group_score))

            if group_score >= 98:
                play_sound_effect('ambient_group_legendary', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)   
            elif group_score >= 95:
                play_sound_effect('ambient_group_perfect', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)
            elif group_score >= 92:
                play_sound_effect('ambient_group_very_nice', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)
            elif group_score >= 89:
                play_sound_effect('ambient_group_good', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)
            elif group_score >= 86:
                play_sound_effect('ambient_group_normal', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)

        ppi("Turn ended")



    if isGameFin == True:
        isGameFinished = True

def process_match_cricket(m):
    currentPlayerIndex = m['player']
    currentPlayer = m['players'][currentPlayerIndex]
    currentPlayerName = str(currentPlayer['name']).lower()
    turns = m['turns'][0]
    variant = m['variant']

    isGameOn = False
    isGameFin = False
    global isGameFinished
    global lastPoints

    # Call every thrown dart
    if CALL_EVERY_DART and turns != None and turns['throws'] != None and len(turns['throws']) >= 1: 
        throwAmount = len(turns['throws'])
        type = turns['throws'][throwAmount - 1]['segment']['bed'].lower()
        field_name = turns['throws'][throwAmount - 1]['segment']['name'].lower()
        field_number = turns['throws'][throwAmount - 1]['segment']['number']

        if field_name == '25':
            field_name = 'sbull'
            
        # ppi("Type: " + str(type) + " - Field-name: " + str(field_name))

        # TODO non single file
        if field_number in SUPPORTED_CRICKET_FIELDS and play_sound_effect(field_name) == False:
            inner_outer = False
            if type == 'singleouter' or type == 'singleinner':
                 inner_outer = play_sound_effect(type)
                 if inner_outer == False:
                    play_sound_effect('single')
            else:
                play_sound_effect(type)

    # Check for matchshot
    if m['winner'] != -1 and isGameFinished == False:
        isGameFin = True

        throwPoints = 0
        lastPoints = ''
        for t in turns['throws']:
            number = t['segment']['number']
            if number in SUPPORTED_CRICKET_FIELDS:
                throwPoints += (t['segment']['multiplier'] * number)
                lastPoints += 'x' + str(t['segment']['name'])
        lastPoints = lastPoints[1:]
        
        matchWon = {
                "event": "match-won",
                "player": currentPlayerName,
                "game": {
                    "mode": variant,
                    "dartsThrownValue": throwPoints                    
                } 
            }
        broadcast(matchWon)

        if play_sound_effect('matchshot') == False:
            play_sound_effect('gameshot')
        play_sound_effect(currentPlayerName, True)
        if AMBIENT_SOUNDS != 0.0:
            if play_sound_effect('ambient_matchshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS) == False:
                play_sound_effect('ambient_gameshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)
        setup_caller()
        ppi('Gameshot and match')

    # Check for gameshot
    elif m['gameWinner'] != -1 and isGameFinished == False:
        isGameFin = True

        throwPoints = 0
        lastPoints = ''
        for t in turns['throws']:
            number = t['segment']['number']
            if number in SUPPORTED_CRICKET_FIELDS:
                throwPoints += (t['segment']['multiplier'] * number)
                lastPoints += 'x' + str(t['segment']['name'])
        lastPoints = lastPoints[1:]
        
        gameWon = {
                "event": "game-won",
                "player": currentPlayerName,
                "game": {
                    "mode": variant,
                    "dartsThrownValue": throwPoints
                } 
            }
        broadcast(gameWon)

        play_sound_effect('gameshot')
        play_sound_effect(currentPlayerName, True)
        if AMBIENT_SOUNDS != 0.0:
            play_sound_effect('ambient_gameshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)
        if RANDOM_CALLER_EACH_LEG:
            setup_caller()
        ppi('Gameshot')
    
    # Check for matchon
    elif m['gameScores'][0] == 0 and m['scores'] == None and turns['throws'] == None and m['round'] == 1 and m['leg'] == 1 and m['set'] == 1:
        isGameOn = True
        isGameFinished = False
        
        matchStarted = {
            "event": "match-started",
            "player": currentPlayerName,
            "game": {
                "mode": variant,
                # TODO: fix
                "special": "TODO"
                }     
            }
        broadcast(matchStarted)

        play_sound_effect(currentPlayerName, False)
        if play_sound_effect('matchon', True) == False:
            play_sound_effect('gameon', True)
        # play only if it is a real match not just legs!
        if AMBIENT_SOUNDS != 0.0 and ('legs' in m and 'sets'):
            if play_sound_effect('ambient_matchon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS) == False:
                play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)
        ppi('Matchon')

    # Check for gameon
    elif m['gameScores'][0] == 0 and m['scores'] == None and turns['throws'] == None and m['round'] == 1:
        isGameOn = True
        isGameFinished = False
        
        gameStarted = {
            "event": "game-started",
            "player": currentPlayerName,
            "game": {
                "mode": variant,
                # TODO: fix
                "special": "TODO"
                }     
            }
        broadcast(gameStarted)

        play_sound_effect(currentPlayerName, False)
        play_sound_effect('gameon', True)
        if AMBIENT_SOUNDS != 0.0:
            play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)
        ppi('Gameon')

    # Check for busted turn
    elif turns['busted'] == True:
        lastPoints = "B"
        isGameFinished = False
        busted = { 
                    "event": "busted",
                    "player": currentPlayerName,
                    "game": {
                        "mode": variant
                    }       
                }
        broadcast(busted)

        play_sound_effect('busted')
        if AMBIENT_SOUNDS != 0.0:
            play_sound_effect('ambient_noscore', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)
        ppi('Busted')

    # Check for 1. Dart
    elif turns != None and turns['throws'] != None and len(turns['throws']) == 1:
        isGameFinished = False

    # Check for 2. Dart
    elif turns != None and turns['throws'] != None and len(turns['throws']) == 2:
        isGameFinished = False

    # Check for 3. Dart - points call
    elif turns != None and turns['throws'] != None and len(turns['throws']) == 3:
        isGameFinished = False

        throwPoints = 0
        lastPoints = ''
        for t in turns['throws']:
            number = t['segment']['number']
            if number in SUPPORTED_CRICKET_FIELDS:
                throwPoints += (t['segment']['multiplier'] * number)
                lastPoints += 'x' + str(t['segment']['name'])
        lastPoints = lastPoints[1:]

        dartsThrown = {
            "event": "darts-thrown",
            "player": currentPlayerName,
            "game": {
                "mode": variant,
                "dartNumber": "3",
                "dartValue": throwPoints,        

            }
        }
        broadcast(dartsThrown)

        play_sound_effect(str(throwPoints))
        if AMBIENT_SOUNDS != 0.0:
            if throwPoints == 0:
                play_sound_effect('ambient_noscore', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)
            elif throwPoints == 180:
                play_sound_effect('ambient_180', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)
            elif throwPoints >= 153:
                play_sound_effect('ambient_150more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)   
            elif throwPoints >= 120:
                play_sound_effect('ambient_120more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)
            elif throwPoints >= 100:
                play_sound_effect('ambient_100more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)
            elif throwPoints >= 50:
                play_sound_effect('ambient_50more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)

        ppi("Turn ended")
    
    # Playerchange
    if isGameOn == False and turns != None and turns['throws'] == None or isGameFinished == True:
        dartsPulled = {
            "event": "darts-pulled",
            "player": str(currentPlayer['name']),
            "game": {
                "mode": variant,
                # TODO: fix
                "pointsLeft": "0",
                # TODO: fix
                "dartsThrown": "3",
                "dartsThrownValue": lastPoints,
                "busted": str(turns['busted'])
                # TODO: fix
                # "darts": [
                #     {"number": "1", "value": "60"},
                #     {"number": "2", "value": "60"},
                #     {"number": "3", "value": "60"}
                # ]
            }
        }
        broadcast(dartsPulled)

        if AMBIENT_SOUNDS != 0.0:
            play_sound_effect('ambient_playerchange', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)
        
        ppi("Next player")

    if isGameFin == True:
        isGameFinished = True

         

def connect_autodarts():
    def process(*args):
        global accessToken

        # Configure client
        keycloak_openid = KeycloakOpenID(server_url = AUTODART_AUTH_URL,
                                            client_id = AUTODART_CLIENT_ID,
                                            realm_name = AUTODART_REALM_NAME,
                                            verify = True)

        # Get Token
        token = keycloak_openid.token(AUTODART_USER_EMAIL, AUTODART_USER_PASSWORD)
        accessToken = token['access_token']
        # ppi(token)


        # Get Ticket
        ticket = requests.post(AUTODART_AUTH_TICKET_URL, headers={'Authorization': 'Bearer ' + token['access_token']})
        # ppi(ticket.text)


        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(AUTODART_WEBSOCKET_URL + ticket.text,
                                on_open = on_open_autodarts,
                                on_message = on_message_autodarts,
                                on_error = on_error_autodarts,
                                on_close = on_close_autodarts)

        ws.run_forever()
    threading.Thread(target=process).start()

def on_open_autodarts(ws):
    try:
        global accessToken
        res = requests.get(AUTODART_BOARDS_URL + AUTODART_USER_BOARD_ID, headers={'Authorization': 'Bearer ' + accessToken})
        # ppi(json.dumps(res.json(), indent = 4, sort_keys = True))

        match_id = res.json()['matchId']
        if match_id != None and match_id != '':  
            m = {
                    "event": "start",
                    "id": match_id
                }
            listen_to_newest_match(m, ws)
            
    except Exception as e:
        ppe('Fetching matches failed', e)


    try:
        ppi('Receiving live information from ' + AUTODART_URL)

        # EXAMPLE:
        # const unsub = MessageBroker.getInstance().subscribe<{ id: string; event: 'start' | 'finish' | 'delete' }>(
        # 'autodarts.boards',
        # id + '.matches',

        # (msg) => {
        #     if (msg.event === 'start') {
        #     setMatchId(msg.id);
        #     } else {
        #     setMatchId(undefined);
        #     }
        # }
        # );
        paramsSubscribeMatchesEvents = {
            "channel": "autodarts.boards",
            "type": "subscribe",
            "topic": AUTODART_USER_BOARD_ID + ".matches"
        }
        ws.send(json.dumps(paramsSubscribeMatchesEvents))

    except Exception as e:
        ppe('WS-Open failed: ', e)

def on_message_autodarts(ws, message):
    def process(*args):
        try:
            global lastMessage
            m = json.loads(message)

            # ppi(json.dumps(m, indent = 4, sort_keys = True))
  
            if m['channel'] == 'autodarts.matches':
                global currentMatch
                data = m['data']

                # ppi('Current Match: ' + currentMatch)
                if('turns' in data and len(data['turns']) >=1):
                    data['turns'][0].pop("id", None)
                    data['turns'][0].pop("createdAt", None)

                if lastMessage != data and currentMatch != None and data['id'] == currentMatch:
                    lastMessage = data

                    # ppi(json.dumps(data, indent = 4, sort_keys = True))

                    variant = data['variant']
                    if variant == 'X01' or variant == 'Random Checkout':
                        process_match_x01(data)
                        
                    elif variant == 'Cricket':
                        process_match_cricket(data)

            elif m['channel'] == 'autodarts.boards':
                data = m['data']
                listen_to_newest_match(data, ws)

        except Exception as e:
            ppe('WS-Message failed: ', e)

    threading.Thread(target=process).start()

def on_close_autodarts(ws, close_status_code, close_msg):
    try:
        ppi("Websocket [" + str(ws.url) + "] closed! " + str(close_msg) + " - " + str(close_status_code))
        ppi("Retry : %s" % time.ctime())
        time.sleep(3)
        connect_autodarts()
    except Exception as e:
        ppe('WS-Close failed: ', e)
    
def on_error_autodarts(ws, error):
    try:
        ppi(error)
    except Exception as e:
        ppe('WS-Error failed: ', e)


def on_open_client(client, server):
    ppi('NEW CLIENT CONNECTED: ' + str(client))

def on_message_client(client, server, message):
    def process(*args):
        try:
            ppi('CLIENT MESSAGE: ' + str(message))

        
            if message.startswith('board'):
                receive_local_board_address()

                if boardManagerAddress != None:
                    if message.startswith('board-start'):
                        msg_splitted = message.split(':')

                        wait = 0.1
                        if len(msg_splitted) > 1:
                            wait = float(msg_splitted[1])
                        if wait == 0.0:
                            wait = 0.5
                        time.sleep(wait)
                        
                        res = requests.put(boardManagerAddress + '/api/detection/start')
                        # res = requests.put(boardManagerAddress + '/api/start')
                        # ppi(res)
                        
                    elif message == 'board-stop':
                        res = requests.put(boardManagerAddress + '/api/detection/stop')
                        # res = requests.put(boardManagerAddress + '/api/stop')
                        # ppi(res)

                    elif message == 'board-reset':
                        res = requests.post(boardManagerAddress + '/api/reset')
                        # ppi(res)

                    else:
                        ppi('This message is not supported')  
                else:
                    ppi('Can not change board-state as board-address is unknown!')  


            elif message.startswith('call'):
                msg_splitted = message.split(':')
                to_call = msg_splitted[1]
                call_parts = to_call.split(' ')
                for cp in call_parts:
                    play_sound_effect(cp, wait_for_last = False, volume_mult = 1.0)
        

        except Exception as e:
            ppe('WS-Message failed: ', e)

    t = threading.Thread(target=process).start()

def on_left_client(client, server):
    ppi('CLIENT DISCONNECTED: ' + str(client))

def broadcast(data):
    def process(*args):
        global server
        server.send_message_to_all(json.dumps(data, indent=2).encode('utf-8'))
    t = threading.Thread(target=process)
    t.start()
    t.join()
   


def mute_audio_background(vol):
    global background_audios
    session_fails = 0
    for session in background_audios:
        try:
            volume = session.SimpleAudioVolume
            if session.Process and session.Process.name() != "autodarts-caller.exe":
                volume.SetMasterVolume(vol, None)
        # Exception as e:
        except:
            session_fails += 1
            # ppe('Failed to mute audio-process', e)

    return session_fails

def unmute_audio_background(mute_vol):
    global background_audios
    current_master = mute_vol
    steps = 0.1
    wait = 0.1
    while(current_master < 1.0):
        time.sleep(wait)          
        current_master += steps
        for session in background_audios:
            try:
                if session.Process and session.Process.name() != "autodarts-caller.exe":
                    volume = session.SimpleAudioVolume
                    volume.SetMasterVolume(current_master, None)
            #  Exception as e:
            except:
                continue
                # ppe('Failed to unmute audio-process', e)
                
def mute_background(mute_vol):
    global background_audios

    muted = False
    waitDefault = 0.1
    waitForMore = 1.0
    wait = waitDefault

    while True:
        time.sleep(wait)
        if mixer.get_busy() == True and muted == False:
            muted = True
            wait = waitForMore
            session_fails = mute_audio_background(mute_vol)

            if session_fails >= 3:
                # ppi('refreshing background audio sessions')
                background_audios = AudioUtilities.GetAllSessions()

        elif mixer.get_busy() == False and muted == True:    
            muted = False
            wait = waitDefault
            unmute_audio_background(mute_vol)  



@app.route('/')
def index():
    return render_template('index.html', host=WEB_HOST, ws_port=HOST_PORT)

@app.route('/sounds/<path:file_id>', methods=['GET'])
def sound(file_id):
    file_id = unquote(file_id)
    file_path = file_id
    if os.name == 'posix':  # Unix/Linux/MacOS
        directory = '/' + os.path.dirname(file_path)
    else:  # Windows
        directory = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    return send_from_directory(directory, file_name)


def start_websocket_server(host, port):
    global server
    server = WebsocketServer(host=host, port=port, loglevel=logging.ERROR)
    server.set_fn_new_client(on_open_client)
    server.set_fn_client_left(on_left_client)
    server.set_fn_message_received(on_message_client)
    server.run_forever()

def start_flask_app(host, port):
    ppi('Visit WEB-CALLER with other devices at "http://' + str(host) + ':' + str(port) + '"')
    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    
    ap.add_argument("-U", "--autodarts_email", required=True, help="Registered email address at " + AUTODART_URL)
    ap.add_argument("-P", "--autodarts_password", required=True, help="Registered password address at " + AUTODART_URL)
    ap.add_argument("-B", "--autodarts_board_id", required=True, help="Registered board-id at " + AUTODART_URL)
    ap.add_argument("-M", "--media_path", required=True, help="Absolute path to your media folder. You can download free sounds at https://freesound.org/")
    ap.add_argument("-MS", "--media_path_shared", required=False, default=DEFAULT_EMPTY_PATH, help="Absolute path to shared media folder (every caller get sounds)")
    ap.add_argument("-V", "--caller_volume", type=float, default=1.0, required=False, help="Set the caller volume between 0.0 (silent) and 1.0 (max)")
    ap.add_argument("-C", "--caller", default=DEFAULT_CALLER, required=False, help="Sets a particular caller")
    ap.add_argument("-R", "--random_caller", type=int, choices=range(0, 2), default=0, required=False, help="If '1', the application will randomly choose a caller each game. It only works when your base-media-folder has subfolders with its files")
    ap.add_argument("-L", "--random_caller_each_leg", type=int, choices=range(0, 2), default=0, required=False, help="If '1', the application will randomly choose a caller each leg instead of each game. It only works when 'random_caller=1'")
    ap.add_argument("-CCP", "--call_current_player", type=int, choices=range(0, 2), default=0, required=False, help="If '1', the application will call who is the current player to throw")
    ap.add_argument("-E", "--call_every_dart", type=int, choices=range(0, 2), default=0, required=False, help="If '1', the application will call every thrown dart")
    ap.add_argument("-ESF", "--call_every_dart_single_files", type=int, choices=range(0, 2), default=1, required=False, help="If '1', the application will call a every dart by using single, dou.., else it uses two separated sounds: single + x (score)")
    ap.add_argument("-PCC", "--possible_checkout_call", type=int, choices=range(0, 2), default=1, required=False, help="If '1', the application will call a possible checkout starting at 170")
    ap.add_argument("-PCCSF", "--possible_checkout_call_single_files", type=int, choices=range(0, 2), default=0, required=False, help="If '1', the application will call a possible checkout by using yr_2-yr_170, else it uses two separated sounds: you_require + x")
    ap.add_argument("-A", "--ambient_sounds", type=float, default=0.0, required=False, help="If > '0.0' (volume), the application will call a ambient_*-Sounds")
    ap.add_argument("-AAC", "--ambient_sounds_after_calls", type=int, choices=range(0, 2), default=0, required=False, help="If '1', the ambient sounds will appear after calling is finished") 
    ap.add_argument("-DL", "--downloads", type=int, choices=range(0, 2), default=DEFAULT_DOWNLOADS, required=False, help="If '1', the application will try to download a curated list of caller-voices")
    ap.add_argument("-DLL", "--downloads_limit", type=int, default=DEFAULT_DOWNLOADS_LIMIT, required=False, help="If '1', the application will try to download a only the X newest caller-voices. -DLN needs to be activated.")
    ap.add_argument("-DLP", "--downloads_path", required=False, default=DEFAULT_DOWNLOADS_PATH, help="Absolute path for temporarly downloads")
    ap.add_argument("-BAV","--background_audio_volume", required=False, type=float, default=0.0, help="Set background-audio-volume between 0.1 (silent) and 1.0 (no mute)")
    ap.add_argument("-WEB", "--web_caller", required=False, type=int, choices=range(0, 3), default=0, help="If '1' the application will host an web-endpoint, '2' it will do '1' and default caller-functionality.")
    ap.add_argument("-WEBP", "--web_caller_port", required=False, type=int, default=DEFAULT_WEB_CALLER_PORT, help="Web-Caller-Port")
    ap.add_argument("-HP", "--host_port", required=False, type=int, default=DEFAULT_HOST_PORT, help="Host-Port")
    ap.add_argument("-DEB", "--debug", type=int, choices=range(0, 2), default=False, required=False, help="If '1', the application will output additional information")
    ap.add_argument("-CC", "--cert_check", type=int, choices=range(0, 2), default=True, required=False, help="If '0', the application won't check any ssl certification")
    ap.add_argument("-MIF", "--mixer_frequency", type=int, required=False, default=DEFAULT_MIXER_FREQUENCY, help="Pygame mixer frequency")
    ap.add_argument("-MIS", "--mixer_size", type=int, required=False, default=DEFAULT_MIXER_SIZE, help="Pygame mixer size")
    ap.add_argument("-MIC", "--mixer_channels", type=int, required=False, default=DEFAULT_MIXER_CHANNELS, help="Pygame mixer channels")
    ap.add_argument("-MIB", "--mixer_buffersize", type=int, required=False, default=DEFAULT_MIXER_BUFFERSIZE, help="Pygame mixer buffersize")
    
    args = vars(ap.parse_args())

    
    AUTODART_USER_EMAIL = args['autodarts_email']                          
    AUTODART_USER_PASSWORD = args['autodarts_password']              
    AUTODART_USER_BOARD_ID = args['autodarts_board_id']        
    AUDIO_MEDIA_PATH = Path(args['media_path'])
    if args['media_path_shared'] != DEFAULT_EMPTY_PATH:
        AUDIO_MEDIA_PATH_SHARED = Path(args['media_path_shared'])
    else:
        AUDIO_MEDIA_PATH_SHARED = DEFAULT_EMPTY_PATH
    AUDIO_CALLER_VOLUME = args['caller_volume']
    CALLER = args['caller']
    RANDOM_CALLER = args['random_caller']   
    RANDOM_CALLER_EACH_LEG = args['random_caller_each_leg']   
    CALL_CURRENT_PLAYER = args['call_current_player']
    CALL_EVERY_DART = args['call_every_dart']
    CALL_EVERY_DART_SINGLE_FILE = args['call_every_dart_single_files']
    POSSIBLE_CHECKOUT_CALL = args['possible_checkout_call']
    POSSIBLE_CHECKOUT_CALL_SINGLE_FILE = args['possible_checkout_call_single_files']
    AMBIENT_SOUNDS = args['ambient_sounds']
    AMBIENT_SOUNDS_AFTER_CALLS = args['ambient_sounds_after_calls']
    DOWNLOADS = args['downloads']
    DOWNLOADS_LIMIT = args['downloads_limit']
    if DOWNLOADS_LIMIT < 0: DOWNLOADS_LIMIT = 0
    DOWNLOADS_PATH = args['downloads_path']
    BACKGROUND_AUDIO_VOLUME = args['background_audio_volume']
    WEB = args['web_caller']
    WEB_PORT = args['web_caller_port']
    HOST_PORT = args['host_port']
    DEBUG = args['debug']
    CERT_CHECK = args['cert_check']
    MIXER_FREQUENCY = args['mixer_frequency']
    MIXER_SIZE = args['mixer_size']
    MIXER_CHANNELS = args['mixer_channels']
    MIXER_BUFFERSIZE = args['mixer_buffersize']



    if DEBUG:
        ppi('Started with following arguments:')
        ppi(json.dumps(args, indent=4))
    
    args_post_check = None
    try:
        if os.path.commonpath([AUDIO_MEDIA_PATH, main_directory]) == main_directory:
            args_post_check = 'AUDIO_MEDIA_PATH resides inside MAIN-DIRECTORY! It is not allowed!'
        if AUDIO_MEDIA_PATH_SHARED != DEFAULT_EMPTY_PATH:
            if os.path.commonpath([AUDIO_MEDIA_PATH_SHARED, main_directory]) == main_directory:
                args_post_check = 'AUDIO_MEDIA_PATH_SHARED resides inside MAIN-DIRECTORY! It is not allowed!'
            elif os.path.commonpath([AUDIO_MEDIA_PATH_SHARED, AUDIO_MEDIA_PATH]) == AUDIO_MEDIA_PATH:
                args_post_check = 'AUDIO_MEDIA_PATH_SHARED resides inside AUDIO_MEDIA_PATH! It is not allowed!'
            elif os.path.commonpath([AUDIO_MEDIA_PATH, AUDIO_MEDIA_PATH_SHARED]) == AUDIO_MEDIA_PATH_SHARED:
                args_post_check = 'AUDIO_MEDIA_PATH resides inside AUDIO_MEDIA_SHARED! It is not allowed!'
            elif AUDIO_MEDIA_PATH == AUDIO_MEDIA_PATH_SHARED:
                args_post_check = 'AUDIO_MEDIA_PATH is equal to AUDIO_MEDIA_SHARED! It is not allowed!'
    except:
        pass
    
    
    global server
    server = None

    global accessToken
    accessToken = None

    global boardManagerAddress
    boardManagerAddress = None

    global lastMessage
    lastMessage = None

    global currentMatch
    currentMatch = None

    global caller
    caller = None

    global lastPoints
    lastPoints = None

    global isGameFinished
    isGameFinished = False

    global background_audios
    background_audios = None



    # Initialize sound-mixer
    mixer.pre_init(MIXER_FREQUENCY, MIXER_SIZE, MIXER_CHANNELS, MIXER_BUFFERSIZE) 
    mixer.init()

    osType = plat
    osName = os.name
    osRelease = platform.release()
    ppi('\r\n', None, '')
    ppi('##########################################', None, '')
    ppi('       WELCOME TO AUTODARTS-CALLER', None, '')
    ppi('##########################################', None, '')
    ppi('VERSION: ' + VERSION, None, '')
    ppi('RUNNING OS: ' + osType + ' | ' + osName + ' | ' + osRelease, None, '')
    ppi('SUPPORTED GAME-VARIANTS: ' + " ".join(str(x) for x in SUPPORTED_GAME_VARIANTS), None, '')
    ppi('\r\n', None, '')


    if CERT_CHECK:
        ssl._create_default_https_context = ssl.create_default_context
    else:
        ppi("WARNING: SSL-cert-verification disabled!")
        ssl._create_default_https_context = ssl._create_unverified_context
        os.environ['PYTHONHTTPSVERIFY'] = '0'
        


    if args_post_check == None: 
        if plat == 'Windows' and BACKGROUND_AUDIO_VOLUME > 0.0:
            try:
                background_audios = AudioUtilities.GetAllSessions()
                audio_muter = threading.Thread(target=mute_background, args=[BACKGROUND_AUDIO_VOLUME])
                audio_muter.start()
            except Exception as e:
                ppe("Background-muter failed!", e)

        try:
            download_callers()
        except Exception as e:
            ppe("Caller-profile fetching failed!", e)

        try:
            setup_caller()
        except Exception as e:
            ppe("Setup callers failed!", e)

        if caller == None:
            ppi('A caller with name "' + str(CALLER) + '" does NOT exist! Please compare your input with list of possible callers and update -C')
        else:
            try:  
                connect_autodarts()

                websocket_server_thread = threading.Thread(target=start_websocket_server, args=(DEFAULT_HOST_IP, HOST_PORT))
                websocket_server_thread.start()

                if WEB > 0:
                    WEB_HOST = get_local_ip_address()
                    flask_app_thread = threading.Thread(target=start_flask_app, args=(DEFAULT_HOST_IP, WEB_PORT))
                    flask_app_thread.start()

                websocket_server_thread.join()

                if WEB > 0:
                    flask_app_thread.join() 

            except Exception as e:
                ppe("Connect failed: ", e)
   
    else:
        ppi('Please check your arguments: ' + args_post_check)
   

time.sleep(30)