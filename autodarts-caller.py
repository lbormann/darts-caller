import os
from pathlib import Path
import time
import json
import platform
import random
import argparse
from urllib.parse import urlparse
from keycloak import KeycloakOpenID
import requests
from pygame import mixer
import websocket
from websocket_server import WebsocketServer
import threading
import logging
logger=logging.getLogger()



DEFAULT_HOST_IP = '0.0.0.0'
DEFAULT_HOST_PORT = 8079
AUTODART_URL = 'https://autodarts.io'
AUTODART_AUTH_URL = 'https://login.autodarts.io/'
AUTODART_AUTH_TICKET_URL = 'https://api.autodarts.io/ms/v0/ticket'
AUTODART_CLIENT_ID = 'autodarts-app'
AUTODART_REALM_NAME = 'autodarts'
AUTODART_MATCHES_URL = 'https://api.autodarts.io/gs/v0/matches/'
AUTODART_BOARDS_URL = 'https://api.autodarts.io/bs/v0/boards/'
AUTODART_WEBSOCKET_URL = 'wss://api.autodarts.io/ms/v0/subscribe?ticket='

DEFAULT_MIXER_FREQUENCY = 44100
DEFAULT_MIXER_SIZE = 32
DEFAULT_MIXER_CHANNELS = 2
DEFAULT_MIXER_BUFFERSIZE = 4096

BOGEY_NUMBERS = [169, 168, 166, 165, 163, 162, 159]
SUPPORTED_CRICKET_FIELDS = [15, 16, 17, 18, 19, 20, 25]
SUPPORTED_GAME_VARIANTS = ['X01', 'Cricket', 'Random Checkout']
VERSION = '1.8.2'
DEBUG = False


def printv(msg, only_debug = False):
    if only_debug == False or (only_debug == True and DEBUG == True):
        print('\r\n>>> ' + str(msg))

def ppjson(js):
    if DEBUG == True:
        print(json.dumps(js, indent = 4, sort_keys = True))

def log_and_print(message, obj):
    logger.exception(message + str(obj))
    
def parseUrl(str):
    parsedUrl = urlparse(str)
    return parsedUrl.scheme + '://' + parsedUrl.netloc + parsedUrl.path.rstrip("/")

def load_callers(path):
    filenames = []
    for root, dirs, files in os.walk(path):
        file_dict = {}
        for filename in files:
            if filename.endswith('.mp3') or filename.endswith('.wav'):
                full_path = os.path.join(root, filename)
                base = os.path.splitext(filename)[0]
                key = base.split('+', 1)[0]
                if key in file_dict:
                    file_dict[key].append(full_path)
                else:
                    file_dict[key] = [full_path]
        if file_dict:
            filenames.append((root, file_dict))
    return filenames

def setup_caller():
    global caller

    callers = load_callers(AUDIO_MEDIA_PATH)
    printv(str(len(callers)) + ' caller(s) ready to call out your Darts!')

    if RANDOM_CALLER == False:
        caller = callers[0]
    else:
        caller = random.choice(callers)

    printv("Your current caller: " + str(os.path.basename(os.path.normpath(caller[0]))) + " knows " + str(len(caller[1].values())) + " Sound(s)")
    printv(caller[1], True)
    caller = caller[1]

def receive_local_board_address():
    try:
        global accessToken
        global boardManagerAddress

        scheme = 'http://'    
        if boardManagerAddress == None or boardManagerAddress == scheme: 
            res = requests.get(AUTODART_BOARDS_URL + AUTODART_USER_BOARD_ID, headers={'Authorization': 'Bearer ' + accessToken})
            board_ip = res.json()['ip']
            boardManagerAddress = scheme + board_ip
            printv('Board-address: ' + boardManagerAddress)  
    except Exception as e:
        log_and_print('Fetching local-board-address failed', e)



def play_sound(pathToFile, waitForLast, volumeMult):
    if waitForLast == True:
        while mixer.get_busy():
            time.sleep(0.1)

    sound = mixer.Sound(pathToFile)
    if AUDIO_CALLER_VOLUME is not None:
        sound.set_volume(AUDIO_CALLER_VOLUME * volumeMult)
    sound.play()
    # printv('Playing: "' + pathToFile + '"', only_debug=True)

def play_sound_effect(event, waitForLast = False, volumeMult = 1.0):
    try:
        global caller
        play_sound(random.choice(caller[event]), waitForLast, volumeMult)
        return True
    except Exception as e:
        printv('Can not play soundfile for event "' + event + '" -> Ignore this or check existance; otherwise convert your file appropriate')
        return False


def listen_to_newest_match(m, ws):
    global currentMatch
    cm = str(currentMatch)

    # look for supported match that match my board-id and take it as ongoing match
    newMatch = None
    if m['variant'] in SUPPORTED_GAME_VARIANTS and m['finished'] == False:
        for p in m['players']:
            if 'boardId' in p and p['boardId'] == AUTODART_USER_BOARD_ID:
                newMatch = m['id']   
                break

    if cm == None or (cm != None and newMatch != None and cm != newMatch):
        printv('Listen to match: ' + newMatch)

        if cm != None:
            paramsUnsubscribeMatchEvents = {
                "type": "unsubscribe",
                "channel": "autodarts.matches",
                "topic": cm + ".state"
            }
            ws.send(json.dumps(paramsUnsubscribeMatchEvents))

        paramsSubscribeMatchEvents = {
            "type": "subscribe",
            "channel": "autodarts.matches",
            "topic": newMatch + ".state"
        }
        ws.send(json.dumps(paramsSubscribeMatchEvents))
        currentMatch = newMatch
    
def process_match_x01(m):
    variant = m['variant']
    currentPlayerIndex = m['player']
    currentPlayer = m['players'][currentPlayerIndex]
    currentPlayerName = str(currentPlayer['name']).lower()
    remainingPlayerScore = m['gameScores'][currentPlayerIndex]
    turns = m['turns'][0]
    points = str(turns['points'])
    pcc_success = False

    isGameOn = False
    isGameFin = False
    global isGameFinished
    global lastPoints
    global accessToken
    global currentMatch

    # Determine "baseScore"-Key
    base = 'baseScore'
    if 'target' in m['settings']:
        base = 'target'
    
    # and len(turns['throws']) == 3 or isGameFinished == True
    if turns != None and turns['throws'] != None:
        lastPoints = points

    # Call every thrown dart
    if CALL_EVERY_DART and turns != None and turns['throws'] != None and len(turns['throws']) >= 1: 
        throwAmount = len(turns['throws'])
        type = turns['throws'][throwAmount - 1]['segment']['bed'].lower()
        field_name = turns['throws'][throwAmount - 1]['segment']['name'].lower()

        if field_name == '25':
            field_name = 'sbull'

        # printv("Type: " + str(type) + " - Field-name: " + str(field_name))

        if play_sound_effect(field_name) == False:
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
        if AMBIENT_SOUNDS != 0.0:
            if play_sound_effect('ambient_matchshot', volumeMult = AMBIENT_SOUNDS) == False:
                play_sound_effect('ambient_gameshot', volumeMult = AMBIENT_SOUNDS)
        setup_caller()
        printv('Gameshot and match')

    # Check for gameshot
    elif m['gameWinner'] != -1 and isGameFinished == False:
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

        play_sound_effect('gameshot')
        play_sound_effect(currentPlayerName, True)
        if AMBIENT_SOUNDS != 0.0:
            play_sound_effect('ambient_gameshot', volumeMult = AMBIENT_SOUNDS)
        if RANDOM_CALLER_EACH_LEG:
            setup_caller()
        printv('Gameshot')

    # Check for matchon
    elif m['settings'][base] == m['gameScores'][0] and turns['throws'] == None and m['leg'] == 1 and m['set'] == 1:
        isGameOn = True
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

        play_sound_effect(currentPlayerName, False)
        if play_sound_effect('matchon', True) == False:
            play_sound_effect('gameon', True)
        # play only if it is a real match not just legs!
        if AMBIENT_SOUNDS != 0.0 and ('legs' in m and 'sets'):
            if play_sound_effect('ambient_matchon', volumeMult = AMBIENT_SOUNDS) == False:
                play_sound_effect('ambient_gameon', volumeMult = AMBIENT_SOUNDS)

        printv('Matchon')

    # Check for gameon
    elif m['settings'][base] == m['gameScores'][0] and turns['throws'] == None:
        isGameOn = True
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

        play_sound_effect(currentPlayerName, False)
        play_sound_effect('gameon', True)
        if AMBIENT_SOUNDS != 0.0:
            play_sound_effect('ambient_gameon', volumeMult = AMBIENT_SOUNDS)

        printv('Gameon')
          
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
            play_sound_effect('ambient_noscore', volumeMult = AMBIENT_SOUNDS)
        printv('Busted')

    # Check for possible checkout
    elif POSSIBLE_CHECKOUT_CALL and m['player'] == currentPlayerIndex and remainingPlayerScore <= 170 and remainingPlayerScore not in BOGEY_NUMBERS and turns != None and turns['throws'] == None:
        isGameFinished = False
        play_sound_effect(currentPlayerName)

        remaining = str(remainingPlayerScore)
        pcc_success = play_sound_effect('yr_' + remaining, True)
        if pcc_success == False:
            pcc_success = play_sound_effect(remaining, True)

        printv('Checkout possible')

    # Check for 1. Dart
    elif turns != None and turns['throws'] != None and len(turns['throws']) == 1:
        isGameFinished = False

    # Check for 2. Dart
    elif turns != None and turns['throws'] != None and len(turns['throws']) == 2:
        isGameFinished = False

    # Check for 3. Dart - points call
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
            if turns['points'] == 0:
                play_sound_effect('ambient_noscore', volumeMult = AMBIENT_SOUNDS)
            elif turns['points'] == 180:
                play_sound_effect('ambient_180', volumeMult = AMBIENT_SOUNDS)
            elif turns['points'] >= 153:
                play_sound_effect('ambient_150more', volumeMult = AMBIENT_SOUNDS)   
            elif turns['points'] >= 120:
                play_sound_effect('ambient_120more', volumeMult = AMBIENT_SOUNDS)
            elif turns['points'] >= 100:
                play_sound_effect('ambient_100more', volumeMult = AMBIENT_SOUNDS)
            elif turns['points'] >= 50:
                play_sound_effect('ambient_50more', volumeMult = AMBIENT_SOUNDS)


        printv("Turn ended")

    # Playerchange
    if isGameOn == False and turns != None and turns['throws'] == None or isGameFinished == True:
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
        broadcast(dartsPulled)

        if pcc_success == False:
            play_sound_effect('playerchange')

        printv("Next player")


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
            
        # printv("Type: " + str(type) + " - Field-name: " + str(field_name))

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
            if play_sound_effect('ambient_matchshot', volumeMult = AMBIENT_SOUNDS) == False:
                play_sound_effect('ambient_gameshot', volumeMult = AMBIENT_SOUNDS)
        setup_caller()
        printv('Gameshot and match')

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
            play_sound_effect('ambient_gameshot', volumeMult = AMBIENT_SOUNDS)
        if RANDOM_CALLER_EACH_LEG:
            setup_caller()
        printv('Gameshot')
    
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
            if play_sound_effect('ambient_matchon', volumeMult = AMBIENT_SOUNDS) == False:
                play_sound_effect('ambient_gameon', volumeMult = AMBIENT_SOUNDS)
        printv('Matchon')

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
            play_sound_effect('ambient_gameon', volumeMult = AMBIENT_SOUNDS)
        printv('Gameon')

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
            play_sound_effect('ambient_noscore', volumeMult = AMBIENT_SOUNDS)
        printv('Busted')

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
                play_sound_effect('ambient_noscore', volumeMult = AMBIENT_SOUNDS)
            elif throwPoints == 180:
                play_sound_effect('ambient_180', volumeMult = AMBIENT_SOUNDS)
            elif throwPoints >= 153:
                play_sound_effect('ambient_150more', volumeMult = AMBIENT_SOUNDS)   
            elif throwPoints >= 120:
                play_sound_effect('ambient_120more', volumeMult = AMBIENT_SOUNDS)
            elif throwPoints >= 100:
                play_sound_effect('ambient_100more', volumeMult = AMBIENT_SOUNDS)
            elif throwPoints >= 50:
                play_sound_effect('ambient_50more', volumeMult = AMBIENT_SOUNDS)

        printv("Turn ended")
    
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

        play_sound_effect('playerchange')
        printv("Next player")

    if isGameFin == True:
        isGameFinished = True


def broadcast(data):
    def process(*args):
        global server
        server.send_message_to_all(json.dumps(data, indent=2).encode('utf-8'))
    threading.Thread(target=process).start()
            

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
        printv(token, only_debug = True)


        # Get Ticket
        ticket = requests.post(AUTODART_AUTH_TICKET_URL, headers={'Authorization': 'Bearer ' + token['access_token']})
        printv(ticket.text, only_debug = True)


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
        printv('Receiving live information from ' + AUTODART_URL)
        printv('!!! In case that calling is not working, please check your Board-ID (-B) for correctness !!!')
        paramsSubscribeMatchesEvents = {
            "channel": "autodarts.matches",
            "type": "subscribe",
            "topic": "*.state"
        }
        ws.send(json.dumps(paramsSubscribeMatchesEvents))

        receive_local_board_address()
    except Exception as e:
        log_and_print('WS-Open failed: ', e)

def on_message_autodarts(ws, message):
    def process(*args):
        try:
            global lastMessage
            m = json.loads(message)

            # ppjson(m)

            if m['channel'] == 'autodarts.matches':
                global currentMatch
                data = m['data']
                listen_to_newest_match(data, ws)

                # printv('Current Match: ' + currentMatch)
                if('turns' in data and len(data['turns']) >=1):
                    data['turns'][0].pop("id", None)
                    data['turns'][0].pop("createdAt", None)

                if lastMessage != data and currentMatch != None and data['id'] == currentMatch:
                    lastMessage = data
                    ppjson(data)

                    variant = data['variant']
                    if variant == 'X01' or variant == 'Random Checkout':
                        process_match_x01(data)
                    elif variant == 'Cricket':
                        process_match_cricket(data)
        except Exception as e:
            log_and_print('WS-Message failed: ', e)

    threading.Thread(target=process).start()

def on_close_autodarts(ws, close_status_code, close_msg):
    try:
        printv("Websocket closed")
        printv(str(close_msg))
        printv(str(close_status_code))
        printv ("Retry : %s" % time.ctime())
        time.sleep(3)
        connect_autodarts()
    except Exception as e:
        log_and_print('WS-Close failed: ', e)
    
def on_error_autodarts(ws, error):
    try:
        printv(error)
    except Exception as e:
        log_and_print('WS-Error failed: ', e)


def client_new_message(client, server, message):
    def process(*args):
        try:
            printv('CLIENT MESSAGE: ' + str(message))

            if boardManagerAddress != None and boardManagerAddress != 'http://':
                if message.startswith('board-start'):
                    msg_splitted = message.split(':')
                    if len(msg_splitted) > 1:
                        time.sleep(float(msg_splitted[1]))
                    res = requests.put(boardManagerAddress + '/api/start')
                    # printv(str(res))

                elif message == 'board-stop':
                    res = requests.put(boardManagerAddress + '/api/stop')
                    # printv(str(res))
            else:
              printv('Can not start board as board-address is unknown: ' + str(boardManagerAddress))  

        except Exception as e:
            log_and_print('WS-Message failed: ', e)
    threading.Thread(target=process).start()

def new_client(client, server):
    printv('NEW CLIENT CONNECTED: ' + str(client))

def client_left(client, server):
    printv('CLIENT DISCONNECTED: ' + str(client))




if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    
    ap.add_argument("-U", "--autodarts_email", required=True, help="Registered email address at " + AUTODART_URL)
    ap.add_argument("-P", "--autodarts_password", required=True, help="Registered password address at " + AUTODART_URL)
    ap.add_argument("-B", "--autodarts_board_id", required=True, help="Registered board-id at " + AUTODART_URL)
    ap.add_argument("-M", "--media_path", required=True, help="Absolute path to your media folder. You can download free sounds at https://freesound.org/")
    ap.add_argument("-V", "--caller_volume", type=float, default=1.0, required=False, help="Set the caller volume between 0.0 (silent) and 1.0 (max)")
    ap.add_argument("-R", "--random_caller", type=int, choices=range(0, 2), default=0, required=False, help="If '1', the application will randomly choose a caller each game. It only works when your base-media-folder has subfolders with its files")
    ap.add_argument("-L", "--random_caller_each_leg", type=int, choices=range(0, 2), default=0, required=False, help="If '1', the application will randomly choose a caller each leg instead of each game. It only works when 'random_caller=1'")
    ap.add_argument("-E", "--call_every_dart", type=int, choices=range(0, 2), default=0, required=False, help="If '1', the application will call every thrown dart")
    ap.add_argument("-PCC", "--possible_checkout_call", type=int, choices=range(0, 2), default=1, required=False, help="If '1', the application will call a possible checkout starting at 170")
    ap.add_argument("-A", "--ambient_sounds", type=float, default=0.0, required=False, help="If > '0.0' (volume), the application will call a ambient_*-Sounds")
    ap.add_argument("-HP", "--host_port", required=False, type=int, default=DEFAULT_HOST_PORT, help="Host-Port")
    ap.add_argument("-MIF", "--mixer_frequency", type=int, required=False, default=DEFAULT_MIXER_FREQUENCY, help="Pygame mixer frequency")
    ap.add_argument("-MIS", "--mixer_size", type=int, required=False, default=DEFAULT_MIXER_SIZE, help="Pygame mixer size")
    ap.add_argument("-MIC", "--mixer_channels", type=int, required=False, default=DEFAULT_MIXER_CHANNELS, help="Pygame mixer channels")
    ap.add_argument("-MIB", "--mixer_buffersize", type=int, required=False, default=DEFAULT_MIXER_BUFFERSIZE, help="Pygame mixer buffersize")
    

    args = vars(ap.parse_args())

    AUTODART_USER_EMAIL = args['autodarts_email']                          
    AUTODART_USER_PASSWORD = args['autodarts_password']              
    AUTODART_USER_BOARD_ID = args['autodarts_board_id']        
    AUDIO_MEDIA_PATH = args['media_path']
    AUDIO_MEDIA_PATH = Path(AUDIO_MEDIA_PATH)
    AUDIO_CALLER_VOLUME = args['caller_volume']
    RANDOM_CALLER = args['random_caller']   
    RANDOM_CALLER_EACH_LEG = args['random_caller_each_leg']   
    CALL_EVERY_DART = args['call_every_dart']
    POSSIBLE_CHECKOUT_CALL = args['possible_checkout_call']
    AMBIENT_SOUNDS = args['ambient_sounds']
    HOST_PORT = args['host_port']
    MIXER_FREQUENCY = args['mixer_frequency']
    MIXER_SIZE = args['mixer_size']
    MIXER_CHANNELS = args['mixer_channels']
    MIXER_BUFFERSIZE = args['mixer_buffersize']

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


    # Initialize sound-output
    mixer.pre_init(MIXER_FREQUENCY, MIXER_SIZE, MIXER_CHANNELS, MIXER_BUFFERSIZE) 
    mixer.init()

    printv('Started with following arguments:')
    printv(json.dumps(args, indent=4))

    osType = platform.system()
    osName = os.name
    osRelease = platform.release()
    print('\r\n')
    print('##########################################')
    print('       WELCOME TO AUTODARTS-CALLER')
    print('##########################################')
    print('VERSION: ' + VERSION)
    print('RUNNING OS: ' + osType + ' | ' + osName + ' | ' + osRelease)
    print('SUPPORTED GAME-VARIANTS: ' + " ".join(str(x) for x in SUPPORTED_GAME_VARIANTS) )
    print('\r\n')
  
    try:
        setup_caller()
        connect_autodarts()
        
        server = WebsocketServer(host=DEFAULT_HOST_IP, port=HOST_PORT, loglevel=logging.ERROR)
        server.set_fn_new_client(new_client)
        server.set_fn_client_left(client_left)
        server.set_fn_message_received(client_new_message)
        server.run_forever()

    except Exception as e:
        log_and_print("Connect failed: ", e)
   
