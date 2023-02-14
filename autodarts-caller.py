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
import threading
import logging
logger=logging.getLogger()




AUTODART_URL = 'https://autodarts.io'
AUTODART_AUTH_URL = 'https://login.autodarts.io/'
AUTODART_AUTH_TICKET_URL = 'https://api.autodarts.io/ms/v0/ticket'
AUTODART_CLIENT_ID = 'autodarts-app'
AUTODART_REALM_NAME = 'autodarts'
AUTODART_MATCHES_URL = 'https://api.autodarts.io/gs/v0/matches'
AUTODART_BOARDS_URL = 'https://api.autodarts.io/bs/v0/boards/'
AUTODART_WEBSOCKET_URL = 'wss://api.autodarts.io/ms/v0/subscribe?ticket='

DEFAULT_MIXER_FREQUENCY = 44100
DEFAULT_MIXER_SIZE = 32
DEFAULT_MIXER_CHANNELS = 2
DEFAULT_MIXER_BUFFERSIZE = 4096

BOGEY_NUMBERS = [169, 168, 166, 165, 163, 162, 159]
SUPPORTED_CRICKET_FIELDS = [15, 16, 17, 18, 19, 20, 25]
SUPPORTED_GAME_VARIANTS = ['X01', 'Cricket', 'Random Checkout']
VERSION = '1.6.1'
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
    

def play_sound(pathToFile, waitForLast, volume_lower):
    if waitForLast == True:
        while mixer.get_busy():
            time.sleep(0.1)

    sound = mixer.Sound(pathToFile)
    if AUDIO_CALLER_VOLUME is not None:
        sound.set_volume(AUDIO_CALLER_VOLUME + volume_lower)
    sound.play()

def play_sound_effect(event, waitForLast = False, volumeLower = 0):
    try:
        global caller
        play_sound(random.choice(caller[event]), waitForLast, volumeLower)
        return True
    except Exception as e:
        log_and_print('Failed to play soundfile for: "' + event + '" -> Check existance of that soundfile if you want to play it: ', e)
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

    # Determine "baseScore"-Key
    base = 'baseScore'
    if 'target' in m['settings']:
        base = 'target'
    
    # and len(turns['throws']) == 3 or isGameFinished == True
    if turns != None and turns['throws'] != None:
        lastPoints = points

    if CALL_EVERY_DART and turns != None and turns['throws'] != None and len(turns['throws']) >= 1: 
        throwAmount = len(turns['throws'])
        type = turns['throws'][throwAmount - 1]['segment']['bed']

        if type == 'Single':
            play_sound_effect('single')
        elif type == 'SingleOuter':
            play_sound_effect('single')
        elif type == 'SingleInner':
            play_sound_effect('single')
        elif type == 'Double':
            play_sound_effect('double')
        elif type == 'Triple':
            play_sound_effect('triple')
        elif type == 'Outside':
            play_sound_effect('missed')

    
    # Check for match end
    if m['winner'] != -1 and isGameFinished == False:
        isGameFin = True
        
        matchWon = {
                "event": "match-won",
                "player": currentPlayerName,
                "game": {
                    "mode": "X01",
                    "turnPoints": points
                } 
            }
        broadcast(matchWon)

        play_sound_effect('gameshot')
        play_sound_effect(currentPlayerName, True)
        if AMBIENT_SOUNDS == True:
            play_sound_effect('ambient_gameshot', volumeLower=-0.4)
        setup_caller()
        printv('Match: Gameshot and match')

    # Check for leg/game end
    elif m['gameWinner'] != -1 and isGameFinished == False:
        isGameFin = True
        
        gameWon = {
                "event": "game-won",
                "player": currentPlayerName,
                "game": {
                    "mode": "X01",
                    "turnPoints": points
                } 
            }
        broadcast(gameWon)

        play_sound_effect('gameshot')
        play_sound_effect(currentPlayerName, True)
        if AMBIENT_SOUNDS == True:
            play_sound_effect('ambient_gameshot', volumeLower=-0.4)
        if RANDOM_CALLER_EACH_LEG:
            setup_caller()
        printv('Match: Gameshot and match')

    # Check for leg start
    elif m['settings'][base] == m['gameScores'][0] and turns['throws'] == None:
        isGameOn = True
        isGameFinished = False
        
        gameStarted = {
            "event": "game-started",
            "player": currentPlayerName,
            "game": {
                "mode": "X01",
                "pointsStart": str(base),
                # TODO: fix
                "special": "TODO"
                }     
            }
        broadcast(gameStarted)

        play_sound_effect(currentPlayerName, False)
        play_sound_effect('gameon', True)
        if AMBIENT_SOUNDS == True:
            play_sound_effect('ambient_gameon', volumeLower=-0.6)
        printv('Match: Gameon')
          
    # Check for busted turn
    elif turns['busted'] == True:
        lastPoints = "B"
        isGameFinished = False
        busted = { 
                    "event": "busted",
                    "player": currentPlayerName,
                    "game": {
                        "mode": "X01"
                    }       
                }
        broadcast(busted)

        play_sound_effect('busted')
        if AMBIENT_SOUNDS == True:
            play_sound_effect('ambient_noscore', volumeLower=-0.4)
        printv('Match: Busted')

    # Check for possible checkout
    elif POSSIBLE_CHECKOUT_CALL and m['player'] == currentPlayerIndex and remainingPlayerScore <= 170 and remainingPlayerScore not in BOGEY_NUMBERS and turns != None and turns['throws'] == None:
        isGameFinished = False
        play_sound_effect(currentPlayerName)

        remaining = str(remainingPlayerScore)
        pcc_success = play_sound_effect('yr_' + remaining, True)
        if pcc_success == False:
            pcc_success = play_sound_effect(remaining, True)

        printv('Match: Checkout possible')

    # Check for 1. Dart
    elif turns != None and turns['throws'] != None and len(turns['throws']) == 1:
        isGameFinished = False

        # if AMBIENT_SOUNDS == True and turns['throws'][0]['segment']['bed'] == 'Outside':
        #     play_sound_effect('ambient_noscore', volumeLower=-0.3)

    # Check for 2. Dart
    elif turns != None and turns['throws'] != None and len(turns['throws']) == 2:
        isGameFinished = False

        # if AMBIENT_SOUNDS == True and turns['throws'][1]['segment']['bed'] == 'Outside':
        #     play_sound_effect('ambient_noscore', volumeLower=-0.3)

    # Check for 3. Dart - points call
    elif turns != None and turns['throws'] != None and len(turns['throws']) == 3:
        isGameFinished = False
        
        dartsThrown = {
            "event": "darts-thrown",
            "player": currentPlayerName,
            "game": {
                "mode": "X01",
                "pointsLeft": str(remainingPlayerScore),
                "dartNumber": "3",
                "dartValue": points,        

            }
        }
        broadcast(dartsThrown)
        
        play_sound_effect(points)
        if AMBIENT_SOUNDS == True:
            if turns['points'] == 0:
                play_sound_effect('ambient_noscore', volumeLower=-0.5)
            elif turns['points'] >= 50:
                play_sound_effect('ambient_50more', volumeLower=-0.4)
            elif turns['points'] >= 100:
                play_sound_effect('ambient_100more', volumeLower=-0.3)
            elif turns['points'] >= 120:
                play_sound_effect('ambient_120more', volumeLower=-0.2)
            elif turns['points'] >= 153:
                play_sound_effect('ambient_150more', volumeLower=-0.1)
            elif turns['points'] == 180:
                play_sound_effect('ambient_180', volumeLower=-0.1)
            

        printv("Match: Turn ended")

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
                "mode": "X01",
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

        printv("Match: Next player")


    if isGameFin == True:
        isGameFinished = True

def process_match_cricket(m):
    currentPlayerIndex = m['player']
    currentPlayer = m['players'][currentPlayerIndex]
    currentPlayerName = str(currentPlayer['name'])
    # remainingPlayerScore = m['gameScores'][currentPlayerIndex]
    turns = m['turns'][0]
    # points = str(turns['points'])

    # TODO: mode/variant by incoming structure

    isGameOn = False
    isGameFin = False
    global isGameFinished
    global lastPoints

    # and len(turns['throws']) == 3 or isGameFinished == True
    # if turns != None and turns['throws'] != None:
    #     lastPoints = points

    if CALL_EVERY_DART and turns != None and turns['throws'] != None and len(turns['throws']) >= 1: 
        throwAmount = len(turns['throws'])
        type = turns['throws'][throwAmount - 1]['segment']['bed']

        if type == 'Single':
            play_sound_effect('single')
        elif type == 'SingleOuter':
            play_sound_effect('single')
        elif type == 'SingleInner':
            play_sound_effect('single')
        elif type == 'Double':
            play_sound_effect('double')
        elif type == 'Triple':
            play_sound_effect('triple')
        elif type == 'Outside':
            play_sound_effect('missed')


    # Check for match end
    if m['winner'] != -1 and isGameFinished == False:
        isGameFin = True
        
        matchWon = {
            "event": "match-won",
            "player": currentPlayerName,
            "game": {
                "mode": "Cricket"
            } 
        }
        broadcast(matchWon)

        play_sound_effect('gameshot')
        setup_caller()
        printv('Match: Gameshot and match')

    # Check for leg/game end
    elif m['gameWinner'] != -1:
        isGameFinished = True

        gameWon = {
                "event": "game-won",
                "player": currentPlayerName,
                "game": {
                    "mode": "Cricket"
                } 
            }
        broadcast(gameWon)
        play_sound_effect('gameshot')
        if RANDOM_CALLER_EACH_LEG:
            setup_caller()
        printv('Match: Gameshot and match')
    
    # Check for leg start
    elif m['gameScores'][0] == 0 and m['scores'] == None and turns['throws'] == None and m['round'] == 1:
        isGameOn = True
        isGameFinished = False

        gameStarted = {
            "event": "game-started",
            "player": currentPlayerName,
            "game": {
                "mode": "Cricket",
                # TODO: fix
                "special": "TODO"
                }     
            }
        broadcast(gameStarted)

        play_sound_effect('gameon')
        printv('Match: Gameon')

    # Check for busted turn
    elif turns['busted'] == True:
        lastPoints = "B"
        isGameFinished = False

        busted = { 
                    "event": "busted",
                    "player": currentPlayerName,
                    "game": {
                        "mode": "X01"
                    }       
                }
        broadcast(busted)

        play_sound_effect('busted')
        printv('Match: Busted')

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
                "mode": "Cricket",
                # "pointsLeft": str(remainingPlayerScore),
                "dartNumber": "3",
                # "dartValue": points,        

            }
        }
        broadcast(dartsThrown)

        play_sound_effect(str(throwPoints))
        printv("Match: Turn ended")
    
    # Playerchange
    if isGameOn == False and turns != None and turns['throws'] == None or isGameFinished == True:
        user = str(currentPlayer['name'])
        throwNumber = "1"
        throwPoints = lastPoints
        pointsLeft = "0"
        busted = str(turns['busted'])
        variant = 'Cricket'

        dartsPulled = {
            "event": "darts-pulled",
            "player": user,
            "game": {
                "mode": variant,
                # TODO: fix
                "pointsLeft": pointsLeft,
                # TODO: fix
                "dartsThrown": "3",
                "dartsThrownValue": throwPoints,
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

        play_sound_effect('playerchange')
        printv("Match: Next player")

    if isGameFin == True:
        isGameFinished = True

        
def broadcast(data):
    for ep in WEBHOOK_THROW_POINTS:
        try:
            threading.Thread(target=broadcast_intern, args=(ep, data)).start()
        except:
            continue

def broadcast_intern(endpoint, data):
    try:
        requests.post(endpoint, json=data, verify=False)      
    except:
        return
            


def connect():
    # Configure client
    keycloak_openid = KeycloakOpenID(server_url = AUTODART_AUTH_URL,
                                        client_id = AUTODART_CLIENT_ID,
                                        realm_name = AUTODART_REALM_NAME,
                                        verify = True)

    # Get Token
    token = keycloak_openid.token(AUTODART_USER_EMAIL, AUTODART_USER_PASSWORD)
    printv(token, only_debug = True)


    # Get Ticket
    ticket = requests.post(AUTODART_AUTH_TICKET_URL, headers={'Authorization': 'Bearer ' + token['access_token']})
    printv(ticket.text, only_debug = True)


    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(AUTODART_WEBSOCKET_URL + ticket.text,
                            on_open = on_open,
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close)

    ws.run_forever()

def on_open(ws):
    try:
        setup_caller()
        printv('Receiving live information from ' + AUTODART_URL)
        printv('!!! In case that calling is not working, please check your Board-ID (-B) for correctness !!!')
        paramsSubscribeMatchesEvents = {
            "channel": "autodarts.matches",
            "type": "subscribe",
            "topic": "*.state"
        }
        ws.send(json.dumps(paramsSubscribeMatchesEvents))
    except Exception as e:
        log_and_print('WS-Open failed: ', e)

def on_message(ws, message):
    try:
        global lastMessage
        m = json.loads(message)

        # ppjson(m)

        if m['channel'] == 'autodarts.matches':
            global currentMatch
            data = m['data']
            listen_to_newest_match(data, ws)

            # printv('Current Match: ' + currentMatch)
            
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

def on_close(ws, close_status_code, close_msg):
    try:
        printv("Websocket closed")
        printv(str(close_msg))
        printv(str(close_status_code))
        printv ("Retry : %s" % time.ctime())
        time.sleep(10)
        connect()
    except Exception as e:
        log_and_print('WS-Close failed: ', e)
    
def on_error(ws, error):
    try:
        printv(error)
    except Exception as e:
        log_and_print('WS-Error failed: ', e)




if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-U", "--autodarts_email", required=True, help="Registered email address at " + AUTODART_URL)
    ap.add_argument("-P", "--autodarts_password", required=True, help="Registered password address at " + AUTODART_URL)
    ap.add_argument("-B", "--autodarts_board_id", required=True, help="Registered board-id at " + AUTODART_URL)
    ap.add_argument("-M", "--media_path", required=True, help="Absolute path to your media folder. You can download free sounds at https://freesound.org/")
    ap.add_argument("-V", "--caller_volume", type=float, required=False, help="Set the caller volume between 0.0 (silent) and 1.0 (max)")
    ap.add_argument("-R", "--random_caller", type=int, choices=range(0, 2), default=0, required=False, help="If '1', the application will randomly choose a caller each game. It only works when your base-media-folder has subfolders with its files")
    ap.add_argument("-L", "--random_caller_each_leg", type=int, choices=range(0, 2), default=0, required=False, help="If '1', the application will randomly choose a caller each leg instead of each game. It only works when 'random_caller=1'")
    ap.add_argument("-E", "--call_every_dart", type=int, choices=range(0, 2), default=0, required=False, help="If '1', the application will call every thrown dart")
    ap.add_argument("-PCC", "--possible_checkout_call", type=int, choices=range(0, 2), default=1, required=False, help="If '1', the application will call a possible checkout starting at 170")
    ap.add_argument("-A", "--ambient_sounds", type=int, choices=range(0, 2), default=0, required=False, help="If '1', the application will call a ambient_*-Sounds")
    ap.add_argument("-WTT", "--webhook_throw_points", required=False, nargs='*', help="Url(s) that will be requested every throw")
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
    WEBHOOK_THROW_POINTS = args['webhook_throw_points']
    CALL_EVERY_DART = args['call_every_dart']
    POSSIBLE_CHECKOUT_CALL = args['possible_checkout_call']
    AMBIENT_SOUNDS = args['ambient_sounds']
    MIXER_FREQUENCY = args['mixer_frequency']
    MIXER_SIZE = args['mixer_size']
    MIXER_CHANNELS = args['mixer_channels']
    MIXER_BUFFERSIZE = args['mixer_buffersize']



    if WEBHOOK_THROW_POINTS is not None:
        parsedList = list()
        for e in WEBHOOK_THROW_POINTS:
            parsedList.append(parseUrl(e))
        WEBHOOK_THROW_POINTS = parsedList
    else:
        WEBHOOK_THROW_POINTS = list()

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
        connect()
    except Exception as e:
        log_and_print("Connect failed: ", e)



    



   
