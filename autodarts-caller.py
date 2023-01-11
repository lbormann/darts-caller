import os
from os import path
from pathlib import Path
import pprint
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



AUTODART_URL = 'https://autodarts.io'
AUTODART_AUTH_URL = 'https://login.autodarts.io/'
AUTODART_AUTH_TICKET_URL = 'https://api.autodarts.io/ms/v0/ticket'
AUTODART_CLIENT_ID = 'autodarts-app'
AUTODART_REALM_NAME = 'autodarts'
AUTODART_MATCHES_URL = 'https://api.autodarts.io/gs/v0/matches'
AUTODART_BOARDS_URL = 'https://api.autodarts.io/bs/v0/boards/'
AUTODART_WEBSOCKET_URL = 'wss://api.autodarts.io/ms/v0/subscribe?ticket='

BOGEY_NUMBERS = [169, 168, 166, 165, 163, 162, 159]
SUPPORTED_CRICKET_FIELDS = [15,16,17,18,19,20,25]
SUPPORTED_GAME_VARIANTS = ['X01', 'Cricket']
VERSION = '1.3.5'
DEBUG = False


def printv(msg, only_debug = False):
    if only_debug == False or (only_debug == True and DEBUG == True):
        print('\r\n>>> ' + str(msg))

def ppjson(js):
    if DEBUG == True:
        print(json.dumps(js, indent = 4, sort_keys = True))

def setup_caller():
    global caller
    if TTS == True:
        import pyttsx3
        pyttsx3.init()
        printv('Your current caller: TTS-Engine')
    else:
        choose_caller()
        printv("Your current caller: " + str(caller))

def choose_caller():
    global caller

    baseMediaPath = AUDIO_MEDIA_PATH

    if RANDOM_CALLER == False:
        caller = baseMediaPath
    else:
        callerSubDirs = [ name for name in os.listdir(AUDIO_MEDIA_PATH) if os.path.isdir(os.path.join(AUDIO_MEDIA_PATH, name)) ]
        printv('Callers available: ' + str(len(callerSubDirs)), only_debug = True)

        if len(callerSubDirs) == 0:
            printv('WARNING: You chose "RANDOM_CALLER", but there are no subfolders that identify your caller-media-files. Please correct this. Fallback to caller-media-files in Media-main-directory.\r\n')
            caller = baseMediaPath
        else:
            caller = os.path.join(baseMediaPath, random.choice(callerSubDirs))


def play_sound(pathToFile):
    if mixer.music.get_busy() == False:
        mixer.music.load(pathToFile)
    else:
        mixer.music.queue(pathToFile)

    if AUDIO_CALLER_VOLUME is not None:
        mixer.music.set_volume(AUDIO_CALLER_VOLUME)
    mixer.music.play()

def play_sound_effect(fileName):
    global caller

    if TTS == True:
        engine.say(fileName)
        engine.runAndWait()
        return

    if osType != 'Linux' and osType != 'Osx' and osType != 'Darwin' and osType != 'Windows': 
        printv('Can not play sound for OS: ' + osType + ". Please contact developer for support") 
        return

    fileToPlay = os.path.join(caller, fileName)
    if path.isfile(fileToPlay + '.wav'):
        play_sound(fileToPlay + '.wav')
    elif path.isfile(fileToPlay + '.mp3'):
        play_sound(fileToPlay + '.mp3')
    else:
        printv('XXX Could not find a playable sound-file for: ' + fileName)


def listen_to_newest_match(m, ws):
    global currentMatch
    cm = str(currentMatch)

    # look for newest supported match that match my board-id and take it as ongoing match
    newMatch = None
    if m['variant'] in SUPPORTED_GAME_VARIANTS and m['finished'] == False:
        for p in m['players']:
            if p['boardId'] == AUTODART_USER_BOARD_ID:
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
    remainingPlayerScore = m['gameScores'][currentPlayerIndex]
    turns = m['turns'][0]
    isGameOn = False
    global lastPoints


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

    
    # Check for game end
    if m['winner'] != -1:
        play_sound_effect('gameshot')
        setup_caller()
        printv('Match: Gameshot and match')

    # Check for leg end
    elif m['gameWinner'] != -1:
        play_sound_effect('gameshot')
        if RANDOM_CALLER_EACH_LEG:
            setup_caller()
        printv('Match: Gameshot and match')

    # Check for leg start
    elif m['settings']['baseScore'] == m['gameScores'][0] and turns['throws'] == None:
        isGameOn = True
        play_sound_effect('gameon')
        printv('Match: Gameon')
          
    # Check for busted turn
    elif turns['busted'] == True:
        play_sound_effect('busted')
        printv('Match: Busted')

    # Check for possible checkout
    elif POSSIBLE_CHECKOUT_CALL and m['player'] == currentPlayerIndex and remainingPlayerScore <= 170 and remainingPlayerScore not in BOGEY_NUMBERS and turns != None and turns['throws'] == None:
        play_sound_effect(str(m['gameScores'][currentPlayerIndex]))
        printv('Match: Checkout possible')

    # Check for points call
    elif turns != None and turns['throws'] != None and len(turns['throws']) == 3:
        points = str(turns['points'])
        lastPoints = points
        play_sound_effect(points)
        printv("Match: Turn ended")

    # Process Webhook
    if isGameOn == False and turns != None and turns['throws'] == None:
        play_sound_effect('playerchange')
        printv("Match: Next player")

        user = str(currentPlayer['name'])
        throwNumber = "0"
        points = lastPoints
        pointsLeft = str(m['gameScores'][currentPlayerIndex])
        busted = str(turns['busted'])
        variant = 'X01'

        throw = user + '/' + throwNumber + '/' + points + '/' + pointsLeft + '/' + busted + '/' + variant
        printv("Match: Throw " + throw)
        call_webhook_throw_points(throw)

def process_match_cricket(m):
    currentPlayerIndex = m['player']
    currentPlayer = m['players'][currentPlayerIndex]
    turns = m['turns'][0]
    isGameOn = False
    global lastPoints


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


    # Check for game end
    if m['winner'] != -1:
        play_sound_effect('gameshot')
        setup_caller()
        printv('Match: Gameshot and match')

    # Check for leg end
    elif m['gameWinner'] != -1:
        play_sound_effect('gameshot')
        if RANDOM_CALLER_EACH_LEG:
            setup_caller()
        printv('Match: Gameshot and match')
    
    # Check for leg start
    elif m['gameScores'][0] == 0 and m['scores'] == None and turns['throws'] == None and m['round'] == 1:
        isGameOn = True
        play_sound_effect('gameon')
        printv('Match: Gameon')

    # Check for busted turn
    elif turns['busted'] == True:
        play_sound_effect('busted')
        printv('Match: Busted')

    # Check for points call
    elif turns != None and turns['throws'] != None and len(turns['throws']) == 3:
        throwPoints = 0
        lastPoints = ''
        for t in turns['throws']:
            number = t['segment']['number']
            if number in SUPPORTED_CRICKET_FIELDS:
                throwPoints += (t['segment']['multiplier'] * number)
                lastPoints += 'x' + str(t['segment']['name'])
        lastPoints = lastPoints[1:]
        play_sound_effect(str(throwPoints))
        printv("Match: Turn ended")
    

    if isGameOn == False and turns != None and turns['throws'] == None:
        play_sound_effect('playerchange')
        printv("Match: Next player")

        user = str(currentPlayer['name'])
        # throwIndex = len(turns['throws']) - 1
        # throwNumber = str(throwIndex + 1)
        throwNumber = "1"
        throwPoints = lastPoints
        pointsLeft = "0"
        busted = str(turns['busted'])
        variant = 'Cricket'

        throw = user + '/' + throwNumber + '/' + throwPoints + '/' + pointsLeft + '/' + busted + '/' + variant
        printv("Match: Throw " + throw)
        call_webhook_throw_points(throw)


def webhook_request(urlii, pathii = None):
    request_url = urlii
    if pathii != None:
        request_url = request_url + "/" + pathii
    else:
        return
    try:
        printv("HTTP: " + request_url)  
        requests.get(request_url, timeout=0.25)     
    except: 
        return

def call_webhook_throw_points(data):
    if WEBHOOK_THROW_POINTS != None:
        webhook_request(WEBHOOK_THROW_POINTS, data)


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
        paramsSubscribeMatchesEvents = {
            "channel": "autodarts.matches",
            "type": "subscribe",
            "topic": "*.state"
        }
        ws.send(json.dumps(paramsSubscribeMatchesEvents))
    except:
        printv("WS-Open failed")

def on_message(ws, message):
    try:
        m = json.loads(message)
        # ppjson(m)

        if m['channel'] == 'autodarts.matches':
            global currentMatch
            data = m['data']
            listen_to_newest_match(data, ws)

            # printv('Current Match: ' + currentMatch)
            
            if currentMatch != None and data['id'] == currentMatch:
                ppjson(data)
                if data['variant'] == 'X01':
                    process_match_x01(data)
                elif data['variant'] == 'Cricket':
                    process_match_cricket(data)
    except:
        printv("WS-Message failed")

def on_close(ws, close_status_code, close_msg):
    try:
        printv("Websocket closed")
        printv(str(close_msg))
        printv(str(close_status_code))
        printv ("Retry : %s" % time.ctime())
        time.sleep(10)
        connect()
    except:
        printv("WS-Close failed")
    
def on_error(ws, error):
    try:
        printv(error)
    except:
        printv("WS-Error failed")




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
    ap.add_argument("-WTT", "--webhook_throw_points", required=False, help="Url that will be requested every throw")
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
    
    if WEBHOOK_THROW_POINTS is not None:
        parsedUrl = urlparse(WEBHOOK_THROW_POINTS)
        WEBHOOK_THROW_POINTS = parsedUrl.scheme + '://' + parsedUrl.netloc + parsedUrl.path.rstrip("/")


    TTS = False     

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
    
    global currentMatch
    currentMatch = None

    global caller
    caller = None

    global lastPoints
    lastPoints = None


    # Initialize sound-output
    mixer.pre_init(44100, -16, 2, 1024)
    mixer.init()


    try:
        connect()
    except:
        printv("Connect failed")


    



   
