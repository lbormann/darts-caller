import os
from dotenv import load_dotenv
import sys
from pathlib import Path
import time
import base64
import platform
import random
import argparse
from custom_argument_parser import CustomArgumentParser
from pygame import mixer
import threading
import logging
import shutil
import re
import csv
import math
import psutil
import queue
from mask import mask
from urllib.parse import quote, unquote
import ssl
from download import download
import json
import certifi
import requests
import websocket
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from assets.autodarts_keycloak_client import AutodartsKeycloakClient
from flask import Flask, render_template, send_from_directory, request
from flask_socketio import SocketIO
from werkzeug.serving import make_ssl_devcert
from engineio.async_drivers import threading as th # IMPORTANT
from assets.get_cred import load_client_credentials, get_client_credentials_from_nodejs_server
from assets.caller_profiles import CALLER_PROFILES
from blind_support import BlindSupport

os.environ['SSL_CERT_FILE'] = certifi.where()

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
app.config['SECRET_KEY'] = 'caller for autodarts'
socketio = SocketIO(app, async_mode="threading")



main_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(main_directory)


VERSION = '2.19.4'


DEFAULT_EMPTY_PATH = ''
DEFAULT_CALLER_VOLUME = 1.0
DEFAULT_CALLER = None
DEFAULT_RANDOM_CALLER = 1
DEFAULT_RANDOM_CALLER_LANGUAGE = 1
DEFAULT_RANDOM_CALLER_GENDER = 0
DEFAULT_CALL_CURRENT_PLAYER = 1
DEFAULT_CALL_BOT_ACTIONS = True
DEFAULT_CALL_EVERY_DART = 0
DEFAULT_CALL_EVERY_DART_TOTAL_SCORE = True
DEFAULT_POSSIBLE_CHECKOUT_CALL = 1
DEFAULT_POSSIBLE_CHECKOUT_CALL_YOURSELF_ONLY = 0
DEFAULT_AMBIENT_SOUNDS = 0.0
DEFAULT_AMBIENT_SOUNDS_AFTER_CALLS = False
DEFAULT_DOWNLOADS = 3
DEFAULT_DOWNLOADS_LANGUAGE = 1
DEFAULT_DOWNLOADS_NAME = None
DEFAULT_REMOVE_OLD_VOICE_PACKS = False
DEFAULT_BACKGROUND_AUDIO_VOLUME = 0.0
DEFAULT_LOCAL_PLAYBACK = True
DEFAULT_WEB_CALLER_DISABLE_HTTPS = False
DEFAULT_HOST_PORT = 8079
DEFAULT_DEBUG = False
DEFAULT_CERT_CHECK = True
DEFAULT_MIXER_FREQUENCY = 44100
DEFAULT_MIXER_SIZE = 32
DEFAULT_MIXER_CHANNELS = 2
DEFAULT_MIXER_BUFFERSIZE = 4096
DEFAULT_DOWNLOADS_PATH = 'caller-downloads-temp'
DEFAULT_CALLERS_BANNED_FILE = 'banned.txt'
DEFAULT_CALLERS_FAVOURED_FILE = 'favoured.txt'
DEFAULT_HOST_IP = '0.0.0.0'
DEFAULT_CALLER_REAL_LIFE = 0
DEFAULT_NODEJS_SERVER_URL = "http://login-darts-caller.peschi.org:3006"
DEFAULT_CALL_BLIND_SUPPORT = 0

EXT_WLED = False
EXT_PIXEL = False
USER_LOCATION = ""
DB_INSERT = 'https://www.user-stats.peschi.org/db_newuserstats.php'
BOARD_OWNER = None
USER_ID = None
DB_ARGS = []
WLED_SETTINGS_ARGS = {}
CALLER_SETTINGS_ARGS = {}

AUTODARTS_CLIENT_ID = None
AUTODARTS_CLIENT_SECRET = None
AUTODARTS_REALM_NAME = 'autodarts'




AUTODARTS_URL = 'https://autodarts.io'
AUTODARTS_AUTH_URL = 'https://login.autodarts.io/'
AUTODARTS_LOBBIES_URL = 'https://api.autodarts.io/gs/v0/lobbies/'
AUTODARTS_MATCHES_URL = 'https://api.autodarts.io/gs/v0/matches/'
AUTODARTS_BOARDS_URL = 'https://api.autodarts.io/bs/v0/boards/'
AUTODARTS_USERS_URL = 'https://api.autodarts.io/as/v0/users/'
AUTODARTS_WEBSOCKET_URL = 'wss://api.autodarts.io/ms/v0/subscribe'
NODEJS_SERVER_URL = "http://login-darts-caller.peschi.org:3006"

SUPPORTED_SOUND_FORMATS = ['.mp3', '.wav']
SUPPORTED_GAME_VARIANTS = ['X01', 'Cricket', 'Random Checkout', 'ATC', 'RTW', 'Count Up', "Bermuda", "Shanghai", "Gotcha"]
SUPPORTED_CRICKET_FIELDS = [15, 16, 17, 18, 19, 20, 25]
SUPPORTED_TACTICS_FIELDS = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25]
BERMUDA_ROUNDS = {
    1: '12',
    2: '13',
    3: '14',
    4: 'D',
    5: '15',
    6: '16',
    7: '17',
    8: 'T',
    9: '18',
    10: '19',
    11: '20',
    12: '25',
    13: '50'
}
BOGEY_NUMBERS = [169, 168, 166, 165, 163, 162, 159]
TEMPLATE_FILE_ENCODING = 'utf-8-sig'



WEB_DB_NAME = "ADC1"

FIELD_COORDS = {
    "0": {"x": 0.016160134143785285,"y": 1.1049884720184449},
    "S1": {"x": 0.2415216935652902,"y": 0.7347516243974009}, 
    "D1": {"x": 0.29786208342066656,"y": 0.9359673024523162}, 
    "T1": {"x": 0.17713267658771747,"y": 0.5818277090756655},
    "S2": {"x": 0.4668832529867955,"y": -0.6415636134982183}, 
    "D2": {"x": 0.5876126598197445,"y": -0.7783902745755609}, 
    "T2": {"x": 0.35420247327604254,"y": -0.4725424439320897},
    "S3": {"x": 0.008111507021588693,"y": -0.7864389016977573}, 
    "D3": {"x": -0.007985747222804492,"y": -0.9715573255082791}, 
    "T3": {"x": -0.007985747222804492,"y": -0.5932718507650387},
    "S4": {"x": 0.6439530496751206,"y": 0.4530496751205198}, 
    "D4": {"x": 0.7888283378746596,"y": 0.5657304548312723}, 
    "T4": {"x": 0.48298050723118835,"y": 0.36451477677635713},
    "S5": {"x": -0.23334730664430925,"y": 0.7508488786417943}, 
    "D5": {"x": -0.31383357786627536,"y": 0.9279186753301195}, 
    "T5": {"x": -0.1850555439111297,"y": 0.5737790819534688},
    "S6": {"x": 0.7888283378746596,"y": -0.013770697966883233}, 
    "D6": {"x": 0.9739467616851814,"y": 0.010375183399706544}, 
    "T6": {"x": 0.5956612869419406,"y": -0.005722070844686641},
    "S7": {"x": -0.4506602389436176,"y": -0.6335149863760215}, 
    "D7": {"x": -0.5713896457765667,"y": -0.7703416474533641}, 
    "T7": {"x": -0.3540767134772585,"y": -0.4725424439320897},
    "S8": {"x": -0.7323621882204988,"y": -0.239132257388388}, 
    "D8": {"x": -0.9255292391532174,"y": -0.2954726472437643}, 
    "T8": {"x": -0.5713896457765667,"y": -0.18279186753301202},
    "S9": {"x": -0.627730035631943,"y": 0.4691469293649132}, 
    "D9": {"x": -0.7726053238314818,"y": 0.5657304548312723}, 
    "T9": {"x": -0.48285474743240414,"y": 0.34841752253196395},
    "S10": {"x": 0.7244393208970865,"y": -0.23108363026619158}, 
    "D10": {"x": 0.9256549989520018,"y": -0.28742402012156787}, 
    "T10": {"x": 0.5715154055753511,"y": -0.19084049465520878},
    "S11": {"x": -0.7726053238314818,"y": -0.005722070844686641}, 
    "D11": {"x": -0.9657723747642004,"y": -0.005722070844686641}, 
    "T11": {"x": -0.5955355271431566,"y": 0.0023265562775099512},
    "S12": {"x": -0.4506602389436176,"y": 0.6140222175644519}, 
    "D12": {"x": -0.5633410186543703,"y": 0.7910920142527772}, 
    "T12": {"x": -0.3540767134772585,"y": 0.4932928107315028},
    "S13": {"x": 0.7244393208970865,"y": 0.24378536994340808}, 
    "D13": {"x": 0.917606371829805,"y": 0.308174386920981}, 
    "T13": {"x": 0.5634667784531546,"y": 0.18744498008803193},
    "S14": {"x": -0.7223277562650692,"y": 0.2440637100898663}, 
    "D14": {"x": -0.9255292391532174,"y": 0.308174386920981}, 
    "T14": {"x": -0.5713896457765667,"y": 0.19549360721022835},
    "S15": {"x": 0.6278557954307273,"y": -0.46449381680989327}, 
    "D15": {"x": 0.7888283378746596,"y": -0.5771745965206456}, 
    "T15": {"x": 0.4910291343533851,"y": -0.34376440997694424},
    "S16": {"x": -0.6196814085097464,"y": -0.4725424439320897}, 
    "D16": {"x": -0.7967512051980717,"y": -0.5610773422762524}, 
    "T16": {"x": -0.49090337455460076,"y": -0.33571578285474746},
    "S17": {"x": 0.2415216935652902,"y": -0.730098511842381}, 
    "D17": {"x": 0.29786208342066656,"y": -0.9152169356529029}, 
    "T17": {"x": 0.18518130370991423,"y": -0.5691259693984492},
    "S18": {"x": 0.48298050723118835,"y": 0.6462167260532384}, 
    "D18": {"x": 0.5554181513309578,"y": 0.799140641374974}, 
    "T18": {"x": 0.3292712798530314,"y": 0.49608083282302506},
    "S19": {"x": -0.2586037966932027,"y": -0.7658909981628906}, 
    "D19": {"x": -0.3134721371708513,"y": -0.9148193508879362}, 
    "T19": {"x": -0.19589712186160443,"y": -0.562094304960196},
    "S20": {"x": 0.00006123698714003468,"y": 0.7939375382731171}, 
    "D20": {"x": 0.01119619445411297, "y": 0.9726766446223462}, 
    "T20": {"x": 0.00006123698714003468, "y": 0.6058175137783223},
    "25": {"x": 0.06276791181873864, "y": 0.01794243723208814}, 
    "50": {"x": -0.007777097366809472, "y": 0.0022657685241886157},
}

CALLER_LANGUAGES = {
    1: ['english', 'en', ],
    2: ['french', 'fr', ],
    3: ['russian', 'ru', ],
    4: ['german', 'de', ],
    5: ['spanish', 'es', ],
    6: ['dutch', 'nl', ],
    7: ['italian', 'it', ],
}
CALLER_GENDERS = {
    1: ['female', 'f'],
    2: ['male', 'm'],
}


def ppi(message, info_object = None, prefix = '\r\n'):
    logger.info(prefix + str(message))
    if info_object != None:
        logger.info(str(info_object))
    
def ppe(message, error_object):
    ppi(message)
    if DEBUG:
        logger.exception("\r\n" + str(error_object))

def get_executable_directory():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    elif __file__:
        return os.path.dirname(os.path.realpath(__file__))
    else:
        raise RuntimeError("Unable to determine executable directory.")

def same_drive(path1, path2):
    drive1 = os.path.splitdrive(path1)[0]
    drive2 = os.path.splitdrive(path2)[0]
    return drive1 == drive2

def check_paths(main_directory, audio_media_path, audio_media_path_shared):
    try:
        main_directory = get_executable_directory()
        errors = None

        audio_media_path = os.path.normpath(audio_media_path)
        
        if audio_media_path_shared != DEFAULT_EMPTY_PATH:
            audio_media_path_shared = os.path.normpath(audio_media_path_shared)

        if same_drive(audio_media_path, main_directory) == True and os.path.commonpath([audio_media_path, main_directory]) == main_directory:
            errors = 'AUDIO_MEDIA_PATH (-M) is a subdirectory of MAIN_DIRECTORY.'

        if audio_media_path_shared != '':
            if same_drive(audio_media_path_shared, main_directory) == True and os.path.commonpath([audio_media_path_shared, main_directory]) == main_directory:
                errors = 'AUDIO_MEDIA_PATH_SHARED (-MS) is a subdirectory of MAIN_DIRECTORY. This is NOT allowed.'
            elif same_drive(audio_media_path_shared, audio_media_path) == True and os.path.commonpath([audio_media_path_shared, audio_media_path]) == audio_media_path:
                errors = 'AUDIO_MEDIA_PATH_SHARED (-MS) is a subdirectory of AUDIO_MEDIA_PATH. This is NOT allowed.'
            elif same_drive(audio_media_path, audio_media_path_shared) == True and os.path.commonpath([audio_media_path, audio_media_path_shared]) == audio_media_path_shared:
                errors = 'AUDIO_MEDIA_PATH (-M) is a subdirectory of AUDIO_MEDIA_SHARED (-MS). This is NOT allowed.'
            elif same_drive(audio_media_path, audio_media_path_shared) == True and audio_media_path == audio_media_path_shared:
                errors = 'AUDIO_MEDIA_PATH (-M) is equal to AUDIO_MEDIA_SHARED (-MS). This is NOT allowed.'


    except Exception as e:
        errors = f'Path validation failed: {e}'

    if errors is not None:
        ppi("main_directory: " + main_directory)
        ppi("audio_media_path: " + str(audio_media_path))
        ppi("audio_media_path_shared: " + str(audio_media_path_shared))

    return errors

def check_already_running():
    max_count = 3 # app (binary) uses 2 processes => max is (2 + 1) as this one here counts also.
    count = 0
    me, extension = os.path.splitext(os.path.basename(sys.argv[0]))
    ppi("Process is " + me)
    for proc in psutil.process_iter(['pid', 'name']):
        proc_name = proc.info['name'].lower()
        proc_name, extension = os.path.splitext(proc_name)
        if proc_name == me:
            count += 1
            if count >= max_count:
                ppi(f"{me} is already running. Exit")
                sys.exit()  
    # ppi("Start info: " + str(count))

def versionize_speaker(speaker_name, speaker_version):
    speaker_versionized = speaker_name
    if speaker_version > 1:
        speaker_versionized = f"{speaker_versionized}-v{speaker_version}"
    return speaker_versionized

def download_callers(): 
    if DOWNLOADS > 0:
        download_list = CALLER_PROFILES

        # versionize, exclude bans, force download-name
        dl_name = DOWNLOADS_NAME
        if dl_name is not None:
            dl_name = dl_name.lower()
    
        downloads_filtered = {}
        for speaker_name, (speaker_download_url, speaker_version) in download_list.items():
            spn = speaker_name.lower()

            speaker_versionized = versionize_speaker(speaker_name, speaker_version)
            speaker_versionized_lower = speaker_versionized.lower()

            if dl_name == spn or dl_name == speaker_versionized.lower():
                downloads_filtered = {}   
                downloads_filtered[speaker_versionized] = speaker_download_url
                break
               
            if speaker_versionized_lower not in caller_profiles_banned and spn not in caller_profiles_banned:  
                # ppi("spn: " + spn)
                # ppi("dl_name: " + dl_name)
                # ppi("speaker_versionized: " + speaker_versionized.lower())
                downloads_filtered[speaker_versionized] = speaker_download_url
         
        download_list = downloads_filtered

        
        if dl_name != DEFAULT_DOWNLOADS_NAME:
            pass
        else:
            # filter for language
            if DOWNLOADS_LANGUAGE > 0:
                downloads_filtered = {}
                for speaker_name, speaker_download_url in download_list.items():
                    caller_language_key = grab_caller_language(speaker_name)
                    if caller_language_key != DOWNLOADS_LANGUAGE:
                        continue
                    downloads_filtered[speaker_name] = speaker_download_url
                download_list = downloads_filtered

            # filter for limit
            if len(download_list) > 0 and DOWNLOADS < len(download_list):
                download_list = {k: download_list[k] for k in list(download_list.keys())[-DOWNLOADS:]}



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

                # ppi("DOWNLOADING voice-pack: " + cpr_name + " ..")

                # clean download-area!
                shutil.rmtree(DOWNLOADS_PATH, ignore_errors=True)
                if os.path.exists(DOWNLOADS_PATH) == False: 
                    os.mkdir(DOWNLOADS_PATH)
                
                # Download caller-profile and extract archive
                dest = os.path.join(DOWNLOADS_PATH, 'download.zip')

                # kind="zip", 
                path = download(cpr_download_url, dest, progressbar=True, replace=False, timeout=15.0, verbose=DEBUG)
                # LOCAL-Download
                # shutil.copyfile('C:\\Users\\Luca\\Desktop\\download.zip', os.path.join(DOWNLOADS_PATH, 'download.zip'))

                ppi("EXTRACTING VOICE-PACK..")

                shutil.unpack_archive(dest, DOWNLOADS_PATH)
                os.remove(dest)
        
                # Find sound-file-archive und extract it
                zip_filename = [f for f in os.listdir(DOWNLOADS_PATH) if f.endswith('.zip')][0]
                dest = os.path.join(DOWNLOADS_PATH, zip_filename)
                shutil.unpack_archive(dest, DOWNLOADS_PATH)
                os.remove(dest)

                # Find folder and rename it properly
                sound_folder = [dirs for root, dirs, files in sorted(os.walk(DOWNLOADS_PATH))][0][0]
                src = os.path.join(DOWNLOADS_PATH, sound_folder)
                dest = os.path.splitext(dest)[0]
                os.rename(src, dest)

                # Find template-file and parse it
                template_file = [f for f in os.listdir(DOWNLOADS_PATH) if f.endswith('.csv')][0]
                template_file = os.path.join(DOWNLOADS_PATH, template_file)
                san_list = list()
                with open(template_file, 'r', encoding=TEMPLATE_FILE_ENCODING) as f:
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
                for i in range(len(san_list)):
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
                ppi('VOICE-PACK ADDED: ' + cpr_name)

            except Exception as e:
                ppe('FAILED TO PROCESS VOICE-PACK: ' + cpr_name, e)
            finally:
                shutil.rmtree(DOWNLOADS_PATH, ignore_errors=True)

def ban_caller(only_change):
    global caller_title
    global caller_title_without_version

    # ban/change not possible as caller is specified by user or current caller is 'None'
    if (CALLER != DEFAULT_CALLER and CALLER != '' and caller_title != '' and caller_title != None):
       return
    
    if only_change:
        ccc_success = play_sound_effect('control_change_caller', wait_for_last = False, volume_mult = 1.0, mod = False)
        if not ccc_success:
            play_sound_effect('control', wait_for_last = False, volume_mult = 1.0, mod = False)
        
    else:
        cbc_success = play_sound_effect('control_ban_caller', wait_for_last = False, volume_mult = 1.0, mod = False)
        if not cbc_success:
            play_sound_effect('control', wait_for_last = False, volume_mult = 1.0, mod = False)


        global caller_profiles_banned
        caller_profiles_banned.append(caller_title_without_version)
        path_to_callers_banned_file = os.path.join(AUDIO_MEDIA_PATH, DEFAULT_CALLERS_BANNED_FILE)   
        with open(path_to_callers_banned_file, 'w') as bcf:
            for cpb in caller_profiles_banned:
                bcf.write(cpb.lower() + '\n')

    mirror_sounds()
    setup_caller(hi=True)
    
def favor_caller(unfavor):
    global caller_title_without_version
    global caller_profiles_favoured

    if caller_title_without_version == '':
        return
    
    if unfavor:
        caller_profiles_favoured.remove(caller_title_without_version)
    else:
        caller_profiles_favoured.append(caller_title_without_version)

    path_to_callers_favoured_file = os.path.join(AUDIO_MEDIA_PATH, DEFAULT_CALLERS_FAVOURED_FILE)   
    with open(path_to_callers_favoured_file, 'w') as fcf:
        for cpf in caller_profiles_favoured:
            fcf.write(cpf.lower() + '\n')

def delete_old_callers():
    if REMOVE_OLD_VOICE_PACKS:
        folders = os.listdir(AUDIO_MEDIA_PATH)

        # store highest version for every voice-pack
        voice_packs = {}

        for folder in folders:
            # check if folder-name fits pattern "name-vX" or "name"
            match = re.match(r"(.+?)(?:-v(\d+))?$", folder)
            if match:
                name = match.group(1)
                version = int(match.group(2)) if match.group(2) else 0

                # updates highest version for that voice-pack
                if name not in voice_packs or version > voice_packs[name]:
                    voice_packs[name] = version

        # deletes all old voice-pack folders
        for folder in folders:
            match = re.match(r"(.+?)(?:-v(\d+))?$", folder)
            if match:
                name = match.group(1)
                version = int(match.group(2)) if match.group(2) else 0

                if version < voice_packs[name]:
                    folder_path = os.path.join(AUDIO_MEDIA_PATH, folder)
                    shutil.rmtree(folder_path)
                    ppi(f"Removed old voice-pack: {folder}")

def load_callers_banned():
    global caller_profiles_banned
    caller_profiles_banned = []
    
    path_to_callers_banned_file = os.path.join(AUDIO_MEDIA_PATH, DEFAULT_CALLERS_BANNED_FILE)
    
    if os.path.exists(path_to_callers_banned_file):
        try:
            with open(path_to_callers_banned_file, 'r') as bcf:
                caller_profiles_banned = list(set(line.strip() for line in bcf))
                display_caller_list(caller_profiles_banned, "BANNED VOICE-PACKS")
        except FileExistsError:
            pass
    else:
        try:
            with open(path_to_callers_banned_file, 'x'):
                ppi(f"'{path_to_callers_banned_file}' created successfully.")
        except Exception as e:
            ppe(f"Failed to create '{path_to_callers_banned_file}'", e)

def load_callers_favoured():
    global caller_profiles_favoured
    caller_profiles_favoured = []
        
    path_to_callers_favoured_file = os.path.join(AUDIO_MEDIA_PATH, DEFAULT_CALLERS_FAVOURED_FILE)
    
    if os.path.exists(path_to_callers_favoured_file):
        try:
            with open(path_to_callers_favoured_file, 'r') as bcf:
                caller_profiles_favoured = list(set(line.strip() for line in bcf))
                display_caller_list(caller_profiles_favoured, "FAVOURED VOICE-PACKS")
        except FileExistsError:
            pass
    else:
        try:
            with open(path_to_callers_favoured_file, 'x'):
                ppi(f"'{path_to_callers_favoured_file}' created successfully.")
        except Exception as e:
            ppe(f"Failed to create '{path_to_callers_favoured_file}'", e)

def load_callers():
    global callers_profiles_all
    callers_profiles_all = []

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
    for root, dirs, files in os.walk(AUDIO_MEDIA_PATH):

        file_dict = {}
        for filename in files:
            if filename.endswith(tuple(SUPPORTED_SOUND_FORMATS)):
                base = os.path.splitext(filename)[0]
                key = base.split('+', 1)[0]

                full_path = os.path.join(root, filename)
                if key in file_dict:
                    file_dict[key].append(full_path)
                else:
                    file_dict[key] = [full_path]
        if file_dict:
            callers_profiles_all.append((root, file_dict))
        
    # add shared-sounds to callers
    for ss_k, ss_v in shared_sounds.items():
        for (root, c_keys) in callers_profiles_all:
            c_keys[ss_k] = ss_v


def display_caller_list(caller_list, text):
    display = f"{text}: {len(caller_list)}"
    ppi(display, None)

    display = f"[ - "
    for c in caller_list:
        display += c + " - "
    display += "]"
    ppi(display)

def grab_caller_name(caller_path):
    caller_name_with_version = os.path.basename(os.path.normpath(caller_path)).lower()
    parts = caller_name_with_version.split('-')
    caller_name_without_version = "-".join(parts[:-1]) if parts[-1].startswith('v') else caller_name_with_version    
    return (caller_name_without_version, caller_name_with_version)

def grab_caller_language(caller_name):
    first_occurrences = []
    caller_name = '-' + caller_name + '-'
    for key in CALLER_LANGUAGES:
        for tag in CALLER_LANGUAGES[key]:
            tag_with_dashes = '-' + tag + '-'
            index = caller_name.find(tag_with_dashes)
            if index != -1:  # find returns -1 if the tag is not found
                first_occurrences.append((index, key))

    if not first_occurrences:  # if the list is empty
        return None

    # Sort the list of first occurrences and get the language of the tag that appears first
    first_occurrences.sort(key=lambda x: x[0])
    return first_occurrences[0][1]

def grab_caller_gender(caller_name):
    first_occurrences = []
    caller_name = '-' + caller_name + '-'
    for key in CALLER_GENDERS:
        for tag in CALLER_GENDERS[key]:
            tag_with_dashes = '-' + tag + '-'
            index = caller_name.find(tag_with_dashes)
            if index != -1:  # find returns -1 if the tag is not found
                first_occurrences.append((index, key))

    if not first_occurrences:  # if the list is empty
        return None

    # Sort the list of first occurrences and get the gender of the tag that appears first
    first_occurrences.sort(key=lambda x: x[0])
    return first_occurrences[0][1]

def filter_most_recent_versions(voices):
    max_versions = {}
    for voice, data in voices:
        parts = voice.split('-')
        key = '-'.join(parts[:-1]) if parts[-1].startswith('v') else voice
        version = int(parts[-1][1:]) if parts[-1].startswith('v') else 0
        if key not in max_versions or version > max_versions[key][0]:
            max_versions[key] = (version, data)
    
    filtered_voices = []
    for voice, data in voices:
        parts = voice.split('-')
        key = '-'.join(parts[:-1]) if parts[-1].startswith('v') else voice
        version = int(parts[-1][1:]) if parts[-1].startswith('v') else 0
        if version == max_versions[key][0]:
            filtered_voices.append((voice, data))
    
    return filtered_voices

def setup_caller(hi = False):
    global callers_profiles_all
    global caller_profiles_banned
    global CALLER
    global caller
    global caller_title
    global caller_title_without_version
    global callers_available
    global caller_profiles_favoured
    caller = None
    caller_title = ''
    caller_title_without_version = ''


    # filter callers by blacklist, language, gender and most recent version
    callers_filtered = []
    for c in callers_profiles_all:
        (caller_name, caller_name_with_version) = grab_caller_name(c[0])

        if caller_name in caller_profiles_banned or caller_name_with_version in caller_profiles_banned:
            continue

        if CALLER != DEFAULT_CALLER and CALLER != '' and caller_name_with_version.startswith(CALLER.lower()):
            pass
        else:
            if RANDOM_CALLER_LANGUAGE != 0:
                caller_language_key = grab_caller_language(caller_name)
                if caller_language_key != RANDOM_CALLER_LANGUAGE:
                    continue
            if RANDOM_CALLER_GENDER != 0:
                caller_gender_key = grab_caller_gender(caller_name)
                if caller_gender_key != RANDOM_CALLER_GENDER:
                    continue      
        callers_filtered.append(c)
    if len(callers_filtered) > 0:
        callers_filtered = filter_most_recent_versions(callers_filtered)
            
    # store available caller names
    callers_available = []
    for cf in callers_filtered:
        (caller_name, caller_name_with_version) = grab_caller_name(cf[0])
        callers_available.append(caller_name)
    
    display_caller_list(callers_available, "AVAILABLE VOICE-PACKS")


    # specific caller
    if CALLER != DEFAULT_CALLER and CALLER != '':
        (wished_caller, wished_caller_with_version) = grab_caller_name(CALLER)
        for cf in callers_filtered:
            (caller_name, caller_name_with_version) = grab_caller_name(cf[0])         

            if caller_name_with_version.startswith(wished_caller_with_version):
                caller = cf
                break
            elif caller_name_with_version.startswith(wished_caller):
                ppi("NOTICE: '" + wished_caller_with_version + "' is an older voice-pack version. I am now using most recent version: " + "'" + caller_name_with_version + "'", None, '')
                caller = cf
                break


    # random caller
    else:
        if len(callers_filtered) > 0:
            if RANDOM_CALLER == 0:
                caller = callers_filtered[0]
            else:
                caller = random.choice(callers_filtered)
        else:
            caller = None

    # set caller
    if caller is not None:
        for sound_file_key, sound_file_values in caller[1].items():
            sound_list = list()
            for sound_file_path in sound_file_values:
                sound_list.append(sound_file_path)
            caller[1][sound_file_key] = sound_list

        (caller_name, caller_name_with_version) = grab_caller_name(caller[0])  
        caller_title = caller_name_with_version
        caller_title_without_version = caller_name

        ppi("", None)
        ppi("CURRENT VOICE-PACK: " + caller_title + " (" + str(len(caller[1].values())) + " Sound-file-keys)", None)
        ppi("", None)
        # ppi(caller[1])
        caller = caller[1]

        welcome_event = {
            "event": "welcome",
            "callersAvailable": callers_available,
            "callersFavoured": caller_profiles_favoured,
            "caller": caller_title_without_version
        }
        broadcast(welcome_event)

        if hi and play_sound_effect('hi', wait_for_last=False):
            mirror_sounds()
    else:
        ppi('NO CALLERS AVAILABLE')


def check_sounds(sounds_list):
    global caller
    all_sounds_available = True
    try:
        for s in sounds_list:
            caller[s]
    except Exception:
        all_sounds_available = False
    return all_sounds_available

def play_sound(sound, wait_for_last, volume_mult, mod, break_last):
    volume = 1.0
    if AUDIO_CALLER_VOLUME is not None:
        volume = AUDIO_CALLER_VOLUME * volume_mult

    global mirror_files
    global caller_title_without_version
    global sound_break_event
    
    mirror_file = {
                "caller": caller_title_without_version,
                "path": quote(sound, safe=""),
                "wait": wait_for_last,
                "volume": volume,
                "mod": mod
            }
    mirror_files.append(mirror_file)

    if LOCAL_PLAYBACK:
        if break_last == True:
            # Signal alle wartenden Schleifen zu stoppen
            sound_break_event.set()
            # stop last sound
            try:
                mixer.stop()
            except Exception as e:
                ppe('Failed to stop last sound', e)
            # Warte kurz, damit wartende Threads das Signal empfangen
            time.sleep(0.05)
            
            # Event zurücksetzen - aber nur wenn kein anderer Thread es gerade nutzt
            # Dies ist sicherer mit einem Lock
            sound_break_event.clear()

        if wait_for_last == True:
            check_interval = 0.01
            max_wait = 30  # Max 30 Sekunden warten
            waited = 0
            
            while mixer.get_busy() and waited < max_wait:
                if sound_break_event.is_set():
                    ppi('Sound waiting loop interrupted by break_last signal')
                    return
                time.sleep(check_interval)
                waited += check_interval
            
            if waited >= max_wait:
                ppi('Sound waiting loop timeout reached')
                return
        # BACKUP FALLS NEUE METHODE NICHT STABIL LÄUFT 
        # if wait_for_last == True:
        #     while mixer.get_busy():
        #         # Prüfe ob ein Break-Signal empfangen wurde
        #         if sound_break_event.is_set():
        #             ppi('Sound waiting loop interrupted by break_last signal')
        #             return  # Verlasse die Funktion ohne Sound abzuspielen
        #         time.sleep(0.01)

             
        

        s = mixer.Sound(sound)
        s.set_volume(volume)
        s.play()

    if DEBUG:
        debug_params = []
        if wait_for_last:
            debug_params.append('wait_for_last=True')
        if break_last:
            debug_params.append('break_last=True')
        if volume_mult != 1.0:
            debug_params.append(f'volume_mult={volume_mult}')
        if mod == False:
            debug_params.append('mod=False')
        
        params_str = ' [' + ', '.join(debug_params) + ']' if debug_params else ''
        ppi('Play: "' + sound + '"' + params_str)
    else:
        ppi('Play: "' + sound + '"')

def play_sound_effect(sound_file_key, wait_for_last = False, volume_mult = 1.0, mod = True, break_last = False):
    try:
        global caller
        play_sound(random.choice(caller[sound_file_key]), wait_for_last, volume_mult, mod, break_last)
        return True
    except Exception as e:
        ppe('Can not play sound for sound-file-key "' + sound_file_key + '" -> Ignore this or check existance; otherwise convert your file appropriate', e)
        return False
    
def mirror_sounds():
    global mirror_files
    if len(mirror_files) != 0: 
        # Example
        # {
        #     "event": "mirror",
        #     "files": [
        #         {
        #             "path": "C:\sounds\luca.mp3",
        #             "wait": False,
        #         },
        #         {
        #             "path": "C:\sounds\you_require.mp3",
        #             "wait": True,
        #         },
        #         {
        #             "path": "C:\sounds\40.mp3",
        #             "wait": True,
        #         }
        #     ]
        # }
        mirror = {
            "event": "mirror",
            "files": mirror_files
        }
        broadcast(mirror)
        mirror_files = []


def start_board():

    try:
        res = requests.put(boardManagerAddress + '/api/detection/start')
        # res = requests.put(boardManagerAddress + '/api/start')
        # ppi(res)
    except Exception as e:
        ppe('Start board failed', e)

def stop_board():
    try:    
        res = requests.put(boardManagerAddress + '/api/detection/stop')
        # res = requests.put(boardManagerAddress + '/api/stop')
        # ppi(res)
    except Exception as e:
        ppe('stop board failed', e)

def reset_board():
    try:
        res = requests.post(boardManagerAddress + '/api/reset')
        # ppi(res)
    except Exception as e:
        ppe('Reset board failed', e)

def calibrate_board():
    if play_sound_effect('control_calibrate', wait_for_last = False, volume_mult = 1.0) == False:
        play_sound_effect('control', wait_for_last = False, volume_mult = 1.0)
    mirror_sounds()

    try:
        res = requests.post(boardManagerAddress + '/api/config/calibration/auto')
        # ppi(res)
    except Exception as e:
        ppe('Calibrate board failed', e)


def get_player_average(user_id, variant = 'x01', limit = '100'):
    # get
    # https://api.autodarts.io/as/v0/users/<user-id>/stats/<variant>?limit=<limit>
    try:
        # res = requests.get(AUTODARTS_USERS_URL + user_id + "/stats/" + variant + "?limit=" + limit, headers={'Authorization': 'Bearer ' + kc.access_token})
        res = requests.get(AUTODARTS_USERS_URL + user_id + "/stats/" + variant + "?limit=" + limit, headers = {'Authorization': f'Bearer {kc.access_token}'})
        m = res.json()
        # ppi(m)
        return m['average']['average']
    except Exception as e:
        ppe('Receive player-stats failed', e)
        return None

def start_match(lobbyId):
    if play_sound_effect('control_start_match', wait_for_last = False, volume_mult = 1.0, mod = False) == False:
        play_sound_effect('control', wait_for_last = False, volume_mult = 1.0, mod = False)
    mirror_sounds()

    # post
    # https://api.autodarts.io/gs/v0/lobbies/<lobby-id>/start
    try:
        global currentMatch
        if currentMatch != None:
            res = requests.post(AUTODARTS_LOBBIES_URL + lobbyId + "/start", headers = {'Authorization': f'Bearer {kc.access_token}'})
            ppi(res)

    except Exception as e:
        ppe('Start match failed', e)

def next_throw():
    if play_sound_effect('control_next', wait_for_last = False, volume_mult = 1.0, mod = False) == False:
        play_sound_effect('control', wait_for_last = False, volume_mult = 1.0, mod = False)
    mirror_sounds()

    # post
    # https://api.autodarts.io/gs/v0/matches/<match-id>/players/next
    try:
        global currentMatch
        if currentMatch != None:
            requests.post(AUTODARTS_MATCHES_URL + currentMatch + "/players/next", headers = {'Authorization': f'Bearer {kc.access_token}'})

    except Exception as e:
        ppe('Next throw failed', e)

def undo_throw():
    if play_sound_effect('control_undo', wait_for_last = False, volume_mult = 1.0, mod = False) == False:
        play_sound_effect('control', wait_for_last = False, volume_mult = 1.0, mod = False)
    mirror_sounds()

    # post
    # https://api.autodarts.io/gs/v0/matches/<match-id>/undo
    try:
        global currentMatch
        if currentMatch != None:
            requests.post(AUTODARTS_MATCHES_URL + currentMatch + "/undo", headers = {'Authorization': f'Bearer {kc.access_token}'})
    except Exception as e:
        ppe('Undo throw failed', e)

def correct_throw(throw_indices, score):
    global currentMatch

    score = FIELD_COORDS[score]
    if currentMatch == None or len(throw_indices) > 3 or score == None:
        return

    cdcs_success = False
    cdcs_global = False
    for tii, ti in enumerate(throw_indices):
        wait = False
        if tii > 0 and cdcs_global == True:
            wait = True
        cdcs_success = play_sound_effect(f'control_dart_correction_{(int(ti) + 1)}', wait_for_last = wait, volume_mult = 1.0, mod = False)
        if cdcs_success:
            cdcs_global = True

    if cdcs_global == False and play_sound_effect('control_dart_correction', wait_for_last = False, volume_mult = 1.0, mod = False) == False:
        play_sound_effect('control', wait_for_last = False, volume_mult = 1.0, mod = False)
    mirror_sounds()

    # patch
    # https://api.autodarts.io/gs/v0/matches/<match-id>/throws
    # {
    #     "changes": {
    #         "1": {
    #              "point": {
    #                  "x": x-coord,
    #                  "y": y-coord
    #               },
    #               "type": "normal | bouncer"    
    #         },
    #         "2": {
    #             ...
    #         }
    #     }
    # }
    try:
        global lastCorrectThrow
        data = {"changes": {}}
        for ti in throw_indices:
            data["changes"][ti] = {"point": score, "type": "normal"}

        # ppi(f'Data: {data}')
        if lastCorrectThrow == None or lastCorrectThrow != data:
            requests.patch(AUTODARTS_MATCHES_URL + currentMatch + "/throws", json=data, headers = {'Authorization': f'Bearer {kc.access_token}'})
            lastCorrectThrow = data
        else:
            lastCorrectThrow = None 

    except Exception as e:
        lastCorrectThrow = None 
        ppe('Correcting throw failed', e)

def next_game():
    if play_sound_effect('control_next_game', wait_for_last = False, volume_mult = 1.0, mod = False) == False:
        play_sound_effect('control', wait_for_last = False, volume_mult = 1.0, mod = False)
    mirror_sounds()

    # post
    # https://api.autodarts.io/gs/v0/matches/<match-id>/games/next
    try:
        global currentMatch
        if currentMatch != None:
            requests.post(AUTODARTS_MATCHES_URL + currentMatch + "/games/next", headers = {'Authorization': f'Bearer {kc.access_token}'})

    except Exception as e:
        ppe('Next game failed', e)

def receive_local_board_address():
    # get
    # https://api.autodarts.io/bs/v0/boards/<board-id>
    try:
        global boardManagerAddress

        if boardManagerAddress == None:
            res = requests.get(AUTODARTS_BOARDS_URL + AUTODART_USER_BOARD_ID, headers = {'Authorization': f'Bearer {kc.access_token}'})
            board_ip = res.json()['ip']
            if board_ip != None and board_ip != '':  
                boardManagerAddress = board_ip
                ppi('Board-address: ' + boardManagerAddress) 
            else:
                boardManagerAddress = None
                ppi('Board-address: UNKNOWN') 

            board_event = {
                "event": "board",
                "boardOnline": boardManagerAddress != None
            }
            broadcast(board_event)
            
    except Exception as e:
        boardManagerAddress = None
        ppe('Fetching local-board-address failed', e)

def listen_to_match(m, ws):
    global currentMatch
    global currentMatchHost
    global currentMatchPlayers
    global indexNameMacro
    global gotcha_last_player_points
    global matchIsActive
    global match_lock

    # EXAMPLE
    # {
    #     "channel": "autodarts.boards",
    #     "data": {
    #         "event": "start",
    #         "id": "82f917d0-0308-2c27-c4e9-f53ef2e98ad2"
    #     },
    #     "topic": "1ba2df53-9a04-51bc-9a5f-667b2c5f315f.matches"  
    # }
    ppi(json.dumps(m, indent = 4, sort_keys = True))
    if 'event' not in m:
        return

    if m['event'] == 'start':
        with match_lock:
            currentMatch = m['id']
            matchIsActive = True
        ppi('Listen to match: ' + currentMatch)
        paramsSubscribeTakeOut = {
            "channel": "autodarts.boards",
            "type": "subscribe",
            "topic": AUTODART_USER_BOARD_ID + ".events"
        }
        ws.send(json.dumps(paramsSubscribeTakeOut))
        reset_checkouts_counter()

        try:
            setup_caller()
        except Exception as e:
            ppe("Setup callers failed!", e)

        # fetch-match
        # get
        # https://api.autodarts.io/gs/v0/matches/<match-id>
        try:
            res = requests.get(AUTODARTS_MATCHES_URL + currentMatch, headers = {'Authorization': f'Bearer {kc.access_token}'})
            m = res.json()
            ppi(json.dumps(m, indent = 4, sort_keys = True))

            currentPlayerName = None
            players = []

            if 'players' in m:
                currentPlayer = m['players'][0]
                currentPlayerName = str(currentPlayer['name']).lower()
                players = m['players']

            if 'variant' not in m:
                return
            
            mode = m['variant']


            if mode == 'Bull-off':
                bullingStart = {
                    "event": "bulling-start"
                }
                broadcast(bullingStart)

                play_sound_effect('bulling_start')



            if mode == 'X01':
                currentMatchPlayers = []
                currentMatchHost = None
               
                if players != []:
                    for p in players:
                        if 'boardId' in p:
                            if currentMatchHost is None and m['host']['id'] == p['userId'] and p['boardId'] == AUTODART_USER_BOARD_ID:
                                currentMatchHost = True
                            else: 
                                currentMatchPlayers.append(p)

                # Determine "baseScore"-Key
                base = 'baseScore'
                if 'target' in m['settings']:
                    base = 'target'

                matchStarted = {
                    "event": "match-started",
                    "id": currentMatch,
                    "me": AUTODART_USER_BOARD_ID,
                    "meHost": currentMatchHost,
                    "players": currentMatchPlayers,
                    "player": currentPlayerName,
                    "game": {
                        "mode": mode,
                        "pointsStart": str(m['settings'][base]),
                        # TODO: fix
                        "special": "TODO"
                        }     
                    }
                broadcast(matchStarted)
            elif mode == 'CountUp':
                currentMatchPlayers = []
                currentMatchHost = None

                if players != []:
                    for p in players:
                        if 'boardId' in p:
                            if currentMatchHost is None and m['host']['id'] == p['userId'] and p['boardId'] == AUTODART_USER_BOARD_ID:
                                currentMatchHost = True
                            else: 
                                currentMatchPlayers.append(p)

                matchStarted = {
                    "event": "match-started",
                    "id": currentMatch,
                    "me": AUTODART_USER_BOARD_ID,
                    "meHost": currentMatchHost,
                    "players": currentMatchPlayers,
                    "player": currentPlayerName,
                    "game": {
                        "mode": mode,
                        # TODO: fix
                        "special": "TODO"
                        }     
                    }
                broadcast(matchStarted)

            elif mode == 'Cricket':
                matchStarted = {
                    "event": "match-started",
                    "player": currentPlayerName,
                    "game": {
                        "mode": mode,
                        # TODO: fix
                        "special": "TODO"
                        }     
                    }
                broadcast(matchStarted)
            
            elif mode == 'Bermuda':
                currentMatchPlayers = []
                currentMatchHost = None

                if players != []:
                    for p in players:
                        if 'boardId' in p:
                            if currentMatchHost is None and m['host']['id'] == p['userId'] and p['boardId'] == AUTODART_USER_BOARD_ID:
                                currentMatchHost = True
                            else: 
                                currentMatchPlayers.append(p)

                matchStarted = {
                    "event": "match-started",
                    "id": currentMatch,
                    "me": AUTODART_USER_BOARD_ID,
                    "meHost": currentMatchHost,
                    "players": currentMatchPlayers,
                    "player": currentPlayerName,
                    "game": {
                        "mode": mode,
                        # TODO: fix
                        "special": "TODO"
                        }     
                    }
                broadcast(matchStarted)

            if mode != 'Bull-off':
                callPlayerNameState = False
                
                if CALLER_REAL_LIFE == 1:
                    # s1_l1_n
                    if 'sets' in m and all(score['legs'] == 0 and score['sets'] == 0 for score in m['scores']):
                        currentLeg = m['scores'][0]['legs']
                        currentSet = m['scores'][0]['sets']
                        if currentSet == 0:
                            currentSet = 1
                        if currentLeg == 0:
                            currentLeg = 1
                        play_sound_effect('s'+ str(currentSet)+'_l'+str(currentLeg)+'_n', wait_for_last= True)
                        if play_sound_effect(currentPlayerName, wait_for_last= True) == False:
                                play_sound_effect('player1', wait_for_last= True)
                        play_sound_effect('first_to_throw', wait_for_last= True)
                    elif 'sets' not in m:
                        play_sound_effect('leg_1', wait_for_last= True)
                        if play_sound_effect(currentPlayerName, wait_for_last= True) == False:
                                play_sound_effect('player1', wait_for_last= True)
                        play_sound_effect('first_to_throw', wait_for_last= True)
                else:
                    if CALL_CURRENT_PLAYER >= 1:
                        callPlayerNameState = play_sound_effect(currentPlayerName)

                    if play_sound_effect('matchon', callPlayerNameState, mod = False) == False:
                        play_sound_effect('gameon', callPlayerNameState, mod = False)

                if AMBIENT_SOUNDS != 0.0 and play_sound_effect('ambient_matchon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                    play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

            mirror_sounds()
            ppi('Matchon -listen to match: ' + currentMatch)

        except Exception as e:
            ppe('Fetching initial match-data failed', e)

        global isGameFinished
        isGameFinished = False

        receive_local_board_address()

        paramsSubscribeMatchesEvents = {
            "channel": "autodarts.matches",
            "type": "subscribe",
            "topic": currentMatch + ".state"
        }

        ws.send(json.dumps(paramsSubscribeMatchesEvents))

        # paramsSubscribeMatchesEvents = {
        #     "channel": "autodarts.matches",
        #     "type": "subscribe",
        #     "topic": currentMatch + ".game-events"
        # }
        # ws.send(json.dumps(paramsSubscribeMatchesEvents))

        
    elif m['event'] == 'finish' or m['event'] == 'delete':
        # Debug-Logging für Fehlerdiagnose
        ppi(f"Received {m['event']} event for match: {m['id']}")
        ppi(f"Current match ID: {currentMatch}")
        ppi(f"Match is active: {matchIsActive}")
        
        # Validierung: Nur beenden wenn Match-ID übereinstimmt und Match aktiv ist
        with match_lock:
            if not matchIsActive:
                ppi(f"WARNING: Ignoring {m['event']} event - match is not active")
                return
                
            if currentMatch is None or currentMatch != m['id']:
                ppi(f"WARNING: Ignoring {m['event']} event - match ID mismatch (current: {currentMatch}, event: {m['id']})")
                return
        
        ppi('Stop listening to match: ' + m['id'])
        ppi('listen to match message'+ 'event: ')

        with match_lock:
            currentMatch = None
            matchIsActive = False
        currentMatchHost = None
        currentMatchPlayers = []
        ppi ("Player index reset")
        gotcha_last_player_points=[]
        indexNameMacro = {}

        paramsUnsubscribeMatchEvents = {  
            "channel": "autodarts.matches",
            "type": "unsubscribe",
            "topic": m['id'] + ".state"
        }
        ws.send(json.dumps(paramsUnsubscribeMatchEvents))

        # paramsUnsubscribeMatchEvents = {
        #     "channel": "autodarts.matches",
        #     "type": "unsubscribe",
        #     "topic": m['id'] + ".game-events"
        # }
        # ws.send(json.dumps(paramsUnsubscribeMatchEvents))
        paramsSubscribeTakeOut = {
            "channel": "autodarts.boards",
            "type": "unsubscribe",
            "topic": AUTODART_USER_BOARD_ID + ".events"
        }
        ws.send(json.dumps(paramsSubscribeTakeOut))
        if m['event'] == 'delete':
            play_sound_effect('matchcancel')
            play_sound_effect('ambient_matchcancel', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
            mirror_sounds()
            ppi('--------DEBUG Match delete')
        # USED TO TURN WLED OFF
        matchEnded = {
            "event": "match-ended",
            "me": AUTODART_USER_BOARD_ID
            }
        ppi('--------DEBUG broadcast match ended')
        broadcast(matchEnded)

# BROADCAST BOARD STATUS FOR WLED
def board_status_message(m):
    if m['data']['event'] == 'Takeout started':
        takeoutStarted = {
            "event": "Board Status",
            "data":{
                "status": "Takeout Started"
            }
        }
        ppi('Broadcast Takeout Started')
        broadcast(takeoutStarted)
    elif m['data']['event'] == 'Takeout finished':
        takeoutFinished = {
            "event": "Board Status",
            "data":{
                "status": "Takeout Finished"
            }
        }
        ppi('Broadcast Takeout Finished')
        broadcast(takeoutFinished)
    elif m['data']['event'] == 'Manual reset':
        manualReset = {
            "event": "Board Status",
            "data":{
                "status": "Manual reset"
            }
        }
        ppi('Broadcast Manual Reset')
        broadcast(manualReset)
    elif m['data']['event'] == 'Stopped':
        boardStopped = {
            "event": "Board Status",
            "data":{
                "status": "Board Stopped"
            }
        }
        ppi('Broadcast Board Stop')
        broadcast(boardStopped)
    elif m['data']['event'] == 'Started':
        boardStarted = {
            "event": "Board Status",
            "data":{
                "status": "Board Started"
            }
        }
        ppi('Broadcast Board Started')
        broadcast(boardStarted)
    elif m['data']['event'] == 'Calibration started':
        calibrationStarted= {
            "event": "Board Status",
            "data":{
                "status": "Calibration Started"
            }
        }
        ppi('Broadcast Calibration Started')
        broadcast(calibrationStarted)
    elif m['data']['event'] == 'Calibration finished':
        calibrationFinished = {
            "event": "Board Status",
            "data":{
                "status": "Calibration Finished"
            }
        }
        ppi('Broadcast Calibration Finished')
        broadcast(calibrationFinished)

def reset_checkouts_counter():
    global checkoutsCounter
    checkoutsCounter = {}

def increase_checkout_counter(player_index, remaining_score):
    global checkoutsCounter

    if player_index not in checkoutsCounter:
        checkoutsCounter[player_index] = {'remaining_score': remaining_score, 'checkout_count': 1}
    else:
        if checkoutsCounter[player_index]['remaining_score'] == remaining_score:
            checkoutsCounter[player_index]['checkout_count'] += 1
        else:
            checkoutsCounter[player_index]['remaining_score'] = remaining_score
            checkoutsCounter[player_index]['checkout_count'] = 1

    return checkoutsCounter[player_index]['checkout_count'] <= POSSIBLE_CHECKOUT_CALL

def checkout_only_yourself(currentPlayer):
    if POSSIBLE_CHECKOUT_CALL_YOURSELF_ONLY:
        if 'boardId' in currentPlayer and currentPlayer['boardId'] == AUTODART_USER_BOARD_ID:
            return True
        else:
            return False
    return True

def process_match_x01(m):
    global currentMatch
    global currentMatchHost
    global currentMatchPlayers
    global isGameFinished
    global lastPoints
    global dart1score
    global dart2score
    global dart3score
    global indexNameMacro
    global blindSupport
    
    variant = m['variant']
    players = m['players']
    currentPlayerIndex = m['player']
    if currentPlayerIndex == 0:
        playerNameCaller = 1
    else:
        playerNameCaller = m['player'] + 1
    currentPlayer = m['players'][currentPlayerIndex]
    currentPlayerName = str(currentPlayer['name']).lower()
    currentPlayerIsBot = (m['players'][currentPlayerIndex]['cpuPPR'] is not None)
    remainingPlayerScore = m['gameScores'][currentPlayerIndex]
    numberOfPlayers = len(m['players'])
    turns = m['turns'][0]
    points = str(turns['points'])
    busted = (turns['busted'] == True)
    matchshot = (m['winner'] != -1 and isGameFinished == False)
    gameshot = (m['gameWinner'] != -1 and isGameFinished == False)
    
    # Determine "baseScore"-Key
    base = 'baseScore'
    if 'target' in m['settings']:
        base = 'target'
    
    matchon = (m['settings'][base] == m['gameScores'][0] and turns['throws'] == [] and m['leg'] == 1 and m['set'] == 1)
    gameon = (m['settings'][base] == m['gameScores'][0] and turns['throws'] == [])


    pcc_success = False
    isGameFin = False

    if turns != None and turns['throws'] != []:
        lastPoints = points
    # ppi(json.dumps(turns, indent = 4, sort_keys = True))
    # Darts pulled (Playerchange and Possible-checkout)
    if gameon == False and turns != None and turns['throws'] == [] or isGameFinished == True:
        busted = "False"
        if lastPoints == "B":
            lastPoints = "0"
            busted = "True"
        
        dartsPulled = {
            "event": "darts-pulled",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
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

            if currentPlayerIsBot == False or CALL_BOT_ACTIONS:

                # Check for possible checkout
                if POSSIBLE_CHECKOUT_CALL and \
                        m['player'] == currentPlayerIndex and \
                        remainingPlayerScore <= 170 and \
                        checkout_only_yourself(currentPlayer):
                    
                    if not increase_checkout_counter(currentPlayerIndex, remainingPlayerScore):
                        if AMBIENT_SOUNDS != 0.0:
                            play_sound_effect('ambient_checkout_call_limit', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    else:
                        remaining = str(remainingPlayerScore)
                        if remainingPlayerScore not in BOGEY_NUMBERS:
                            if CALL_CURRENT_PLAYER >= 1:
                                # play_sound_effect(currentPlayerName)
                                if play_sound_effect(currentPlayerName, wait_for_last= True) == False:
                                    play_sound_effect('player'+str(playerNameCaller), wait_for_last= True)

                            pcc_success = play_sound_effect('you_require', True)
                            if pcc_success:
                                if play_sound_effect('c_' + remaining, True) == False:
                                    play_sound_effect(remaining, True)
                            else:
                                pcc_success = play_sound_effect('yr_' + remaining, True)
                            
                            ppi('Checkout possible: ' + remaining)
                        else:
                            if AMBIENT_SOUNDS != 0.0:
                                if play_sound_effect('ambient_bogey_number_' + remaining, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                                    play_sound_effect('ambient_bogey_number', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                            ppi('bogey-number: ' + remaining)

                if pcc_success == False and CALL_CURRENT_PLAYER == 2 and numberOfPlayers > 1:
                    play_sound_effect(currentPlayerName)

            # Player-change
            if pcc_success == False and AMBIENT_SOUNDS != 0.0:
                if play_sound_effect('ambient_playerchange_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                    play_sound_effect('ambient_playerchange', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                

            ppi("Next player")

    # BLIND SUPPORT: Announce dart position (independent of CALL_EVERY_DART)
    if CALL_BLIND_SUPPORT == 1 and turns != None and turns['throws'] != [] and len(turns['throws']) >= 1 and busted == False and matchshot == False and gameshot == False:
        # Skip bot throws - only announce for human players
        if currentPlayerIsBot == False:
            lastThrow = turns['throws'][-1]
            blindSupport.announce_dart_result('X01', lastThrow)
            
            throwAmount = len(turns['throws'])
            
            # After 1st and 2nd dart: announce "you require"
            if throwAmount < 3:
                # remainingPlayerScore is already updated with current throws
                # Just announce "you require" if in checkout range (2-170) and not busted
                if remainingPlayerScore > 0 and remainingPlayerScore <= 170 and remainingPlayerScore not in BOGEY_NUMBERS:
                    blindSupport.announce_remaining_score(remainingPlayerScore)

    # Call every thrown dart
    elif CALL_EVERY_DART > 0 and turns != None and turns['throws'] != [] and len(turns['throws']) >= 1 and busted == False and matchshot == False and gameshot == False: 
        
        if currentPlayerIsBot == False or CALL_BOT_ACTIONS:
            throwAmount = len(turns['throws'])
            type = turns['throws'][throwAmount - 1]['segment']['bed'].lower()
            field_name = turns['throws'][throwAmount - 1]['segment']['name'].lower()
            field_multiplier = turns['throws'][throwAmount - 1]['segment']['multiplier']
            field_number = turns['throws'][throwAmount - 1]['segment']['number']
            # ppi("Type: " + str(type) + " - Field-name: " + str(field_name))
            # ppi(turns['throws'][throwAmount - 1]['segment'])
                

            # SINGLE-DART-SCORE
            if CALL_EVERY_DART == 1:
                score = field_number * field_multiplier
                play_sound_effect(str(score), break_last = True)

            # SINGLE-DART-NAME
            elif CALL_EVERY_DART == 2:
                if field_number == 25 and field_multiplier == 1:
                    field_name = 'bull'
                elif field_number == 25 and field_multiplier == 2:
                    field_name = 'bullseye'

                # bull
                # bullseye 
                # s1 to t20
                # m1 to m20
                if play_sound_effect(field_name, break_last = True) == False:
                    field_number = str(field_number)

                    if type == 'singleouter' or type == 'singleinner':
                        play_sound_effect(field_number, break_last = True)
                    elif type == 'outside':
                        play_sound_effect(type)
                    else:
                        if play_sound_effect(type):
                            play_sound_effect(field_number, wait_for_last=True)

            # SINGLE-DART-EFFECT
            elif CALL_EVERY_DART == 3:
                if field_number == 25 and field_multiplier == 1:
                    field_name = 'bull'
                elif field_number == 25 and field_multiplier == 2:
                    field_name = 'bullseye'

                # effect_bull
                # effect_bullseye 
                # effect_s1 to effect_t20
                # effect_m1 to effect_m20
                if play_sound_effect('effect_' + field_name, mod = False) == False:

                    # effect_single
                    # effect_singleouter
                    # effect_singleinner
                    inner_outer = False
                    if type == 'singleouter' or type == 'singleinner':
                        inner_outer = play_sound_effect('effect_' + type, mod = False)
                        if inner_outer == False:
                            play_sound_effect('effect_single', mod = False)

                    # effect_double
                    # effect_triple 
                    # effect_outside
                    else:
                        play_sound_effect('effect_' + type, mod = False)
            
        
    # Check for matchshot
    if matchshot == True:
        isGameFin = True
        # TEST FÜR DARTS STATS
        throwAmount = len(turns['throws'])
        type = turns['throws'][throwAmount - 1]['segment']['bed'].lower()
        field_name = turns['throws'][throwAmount - 1]['segment']['name'].lower()
        field_multiplier = turns['throws'][throwAmount - 1]['segment']['multiplier']
        field_number = turns['throws'][throwAmount - 1]['segment']['number']
        field_cords_x = turns['throws'][throwAmount - 1]['coords']['x']
        field_cords_y = turns['throws'][throwAmount - 1]['coords']['y']
        # TEST FÜR DARTS STATS
        matchWon = {
                "event": "match-won",
                "player": currentPlayerName,
                "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
                "game": {
                    "mode": variant,
                    "dartsThrown": str(throwAmount),
                    "dartsThrownValue": points,
                    "fieldName": field_name,
                    "fieldNumber": field_number,
                    "fieldMultiplier": field_multiplier,
                    "coords": {
                        "x": field_cords_x,
                        "y": field_cords_y
                    },
                    "type": type
                    
                } 
            }
        broadcast(matchWon)

        if play_sound_effect('matchshot') == False:
            play_sound_effect('gameshot')

        if CALL_CURRENT_PLAYER >= 1:
            play_sound_effect(currentPlayerName, True)

        if AMBIENT_SOUNDS != 0.0:
            if play_sound_effect('ambient_matchshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            elif play_sound_effect('ambient_matchshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            elif play_sound_effect('ambient_gameshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            else:
                play_sound_effect('ambient_gameshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
            

        if RANDOM_CALLER == 2:
            setup_caller()
        ppi('Gameshot and match')

    # Check for gameshot
    elif gameshot == True:
        isGameFin = True
        throwAmount = len(turns['throws'])
        type = turns['throws'][throwAmount - 1]['segment']['bed'].lower()
        field_name = turns['throws'][throwAmount - 1]['segment']['name'].lower()
        field_multiplier = turns['throws'][throwAmount - 1]['segment']['multiplier']
        field_number = turns['throws'][throwAmount - 1]['segment']['number']
        
        gameWon = {
                "event": "game-won",
                "player": currentPlayerName,
                "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
                "game": {
                    "mode": variant,
                    "dartsThrown": str(throwAmount),
                    "dartsThrownValue": points,
                    "fieldName": field_name,
                    "fieldNumber": field_number,
                    "fieldMultiplier": field_multiplier
                } 
            }
        broadcast(gameWon)

        gameshotState = play_sound_effect('gameshot')

        currentPlayerScoreLegs = m['scores'][currentPlayerIndex]['legs']
        # currentPlayerScoreSets = m['scores'][currentPlayerIndex]['sets']
        currentLeg = m['leg']
        currentSet = m['set']
        # maxLeg = m['legs']
        # maxSets = m['sets']

        # ppi('currentLeg: ' + str(currentLeg))
        # ppi('currentSet: ' + str(currentSet))

        isSet = False
        if 'sets' not in m:
            if CALLER_REAL_LIFE == 1:
                play_sound_effect('gameshot_l' + str(currentLeg)+"_n", wait_for_last= True)                
            else:
                play_sound_effect('leg_' + str(currentLeg), gameshotState)
        else:
            if currentPlayerScoreLegs == 0:
                play_sound_effect('set_' + str(currentSet), gameshotState)
                isSet = True
            else:
                if CALLER_REAL_LIFE == 1:
                    # s10_l1_n
                    play_sound_effect('s'+ str(currentSet) + '_l' + str(currentLeg) + "_n", wait_for_last= True)
                else:
                    play_sound_effect('leg_' + str(currentLeg), gameshotState)    

        if CALL_CURRENT_PLAYER >= 1:
            if play_sound_effect(currentPlayerName, wait_for_last= True) == False:
                    play_sound_effect('player'+str(playerNameCaller), wait_for_last= True)

        if AMBIENT_SOUNDS != 0.0:
            if isSet == True:
                if play_sound_effect('ambient_setshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                    pass
                elif play_sound_effect('ambient_setshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                    pass
                elif play_sound_effect('ambient_gameshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                    pass
                else:
                    play_sound_effect('ambient_gameshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    
            else:
                if play_sound_effect('ambient_gameshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                    pass
                else:
                    play_sound_effect('ambient_gameshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

        if RANDOM_CALLER == 2:
            setup_caller()
        ppi('Gameshot')

    # Check for matchon
    elif matchon == True:
        isGameFinished = False
        currentLeg = m['leg']
        currentSet = m['set']

        reset_checkouts_counter()

        currentMatchPlayers = []
        currentMatchHost = None
        if players != []:
            for p in players:
                if 'boardId' in p:
                    if currentMatchHost is None and m['host']['id'] == p['userId'] and p['boardId'] == AUTODART_USER_BOARD_ID:
                        currentMatchHost = True
                    else:
                        currentMatchPlayers.append(p)

        matchStarted = {
            "event": "match-started",
            "id": currentMatch,
            "me": AUTODART_USER_BOARD_ID,
            "meHost": currentMatchHost,
            # "players": currentMatchPlayers,
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "game": {
                "mode": variant,
                "pointsStart": str(m['settings'][base]),
                # TODO: fix
                "special": "TODO"
                }     
            }
        broadcast(matchStarted)

        callPlayerNameState = False
        if CALLER_REAL_LIFE == 1:
            # s1_l1_n
            ppi('new mode')
            play_sound_effect('s'+ str(currentSet)+'_l'+str(currentLeg)+'_n', wait_for_last= True)
            if play_sound_effect(currentPlayerName, wait_for_last= True) == False:
                    play_sound_effect('player'+str(playerNameCaller), wait_for_last= True)
            play_sound_effect('first_to_throw', wait_for_last= True)
        else:
            if CALL_CURRENT_PLAYER >= 1:
                if play_sound_effect(currentPlayerName, wait_for_last= True) == False:
                    play_sound_effect('player'+str(playerNameCaller), wait_for_last= True)

            if play_sound_effect('matchon', callPlayerNameState, mod = False) == False:
                play_sound_effect('gameon', callPlayerNameState, mod = False)

        if AMBIENT_SOUNDS != 0.0:
            state = play_sound_effect('ambient_matchon_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
            if state == False and play_sound_effect('ambient_matchon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                if play_sound_effect('ambient_gameon_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                    play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)


        ppi('Matchon')

    # Check for gameon
    elif gameon == True:
        isGameFinished = False
        # ppi(json.dumps(m, indent = 4, sort_keys = True))

        reset_checkouts_counter()

        gameStarted = {
            "event": "game-started",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "game": {
                "mode": variant,
                "pointsStart": str(m['settings'][base]),
                # TODO: fix
                "special": "TODO"
                }     
            }
        broadcast(gameStarted)

        callPlayerNameState = False
        #### nach legwechsel wird das hier ausgegeben
        ### anpassen auf caller real life
        currentLeg = m['leg']
        currentSet = m['set']
        # maxLeg = m['legs']
        # maxSets = m['sets']

        # ppi('currentLeg: ' + str(currentLeg))
        # ppi('currentSet: ' + str(currentSet))
        if m['stats'][0]['legStats']['dartsThrown'] == 0:
            if CALLER_REAL_LIFE == 1:
                ppi('new mode')
                play_sound_effect('s'+ str(currentSet)+'_l'+str(currentLeg)+'_n', wait_for_last= True)
                
                if play_sound_effect(currentPlayerName, wait_for_last= True) == False:
                        play_sound_effect('player'+str(playerNameCaller), wait_for_last= True)
                play_sound_effect('first_to_throw', wait_for_last= True)
            else:
                if CALL_CURRENT_PLAYER >= 1:
                    if play_sound_effect(currentPlayerName, wait_for_last= True) == False:
                        play_sound_effect('player'+str(playerNameCaller), wait_for_last= True)

                play_sound_effect('gameon', callPlayerNameState, mod = False)

            if AMBIENT_SOUNDS != 0.0:
                if play_sound_effect('ambient_gameon_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                    play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

            ppi('Gameon')
          
    # Check for busted turn
    elif busted == True:
        lastPoints = "B"
        isGameFinished = False
        throwAmount = len(turns['throws'])
        type = turns['throws'][throwAmount - 1]['segment']['bed'].lower()
        field_name = turns['throws'][throwAmount - 1]['segment']['name'].lower()
        field_multiplier = turns['throws'][throwAmount - 1]['segment']['multiplier']
        field_number = turns['throws'][throwAmount - 1]['segment']['number']

        busted = { 
                    "event": "busted",
                    "player": currentPlayerName,
                    "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
                    "playerIsBot": str(currentPlayerIsBot),
                    "game": {
                        "mode": variant,
                        "field_name": field_name,
                        "field_number": field_number,
                        "field_multiplier": field_multiplier,
                        "type": type,
                        "busted": "True",
                    }       
                }
        broadcast(busted)

        if currentPlayerIsBot == False or CALL_BOT_ACTIONS:
            play_sound_effect('busted', mod = False)

            if AMBIENT_SOUNDS != 0.0:
                play_sound_effect('ambient_noscore', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

        ppi('Busted')
    
    # Check for 1. Dart
    elif turns != None and turns['throws'] != [] and len(turns['throws']) == 1:
        isGameFinished = False
        throwAmount = len(turns['throws'])
        type = turns['throws'][throwAmount - 1]['segment']['bed'].lower()
        field_name = turns['throws'][throwAmount - 1]['segment']['name'].lower()
        field_multiplier = turns['throws'][throwAmount - 1]['segment']['multiplier']
        field_number = turns['throws'][throwAmount - 1]['segment']['number']
        field_cords_x = turns['throws'][throwAmount - 1]['coords']['x']
        field_cords_y = turns['throws'][throwAmount - 1]['coords']['y']
        dart1score = points
        dart1Thrown = {
            "event": "dart1-thrown",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "playerIsBot": str(currentPlayerIsBot),
            "game": {
                "mode": variant,
                "pointsLeft": str(remainingPlayerScore),
                "dartNumber": "1",
                "dartValue": points,
                "fieldName": field_name,
                "fieldNumber": field_number,
                "fieldMultiplier": field_multiplier,
                "coords": {
                        "x": field_cords_x,
                        "y": field_cords_y
                    },
                "type": type    
            }
        }
        broadcast(dart1Thrown)

    # Check for 2. Dart
    elif turns != None and turns['throws'] != [] and len(turns['throws']) == 2:
        isGameFinished = False
        throwAmount = len(turns['throws'])
        type = turns['throws'][throwAmount - 1]['segment']['bed'].lower()
        field_name = turns['throws'][throwAmount - 1]['segment']['name'].lower()
        field_multiplier = turns['throws'][throwAmount - 1]['segment']['multiplier']
        field_number = turns['throws'][throwAmount - 1]['segment']['number']
        field_cords_x = turns['throws'][throwAmount - 1]['coords']['x']
        field_cords_y = turns['throws'][throwAmount - 1]['coords']['y']
        dart2score = str(int(points) - int(dart1score))
        dart2Thrown = {
            "event": "dart2-thrown",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "playerIsBot": str(currentPlayerIsBot),
            "game": {
                "mode": variant,
                "pointsLeft": str(remainingPlayerScore),
                "dartNumber": "2",
                "dartValue": dart2score,
                "fieldName": field_name,
                "fieldNumber": field_number,
                "fieldMultiplier": field_multiplier,
                "coords": {
                        "x": field_cords_x,
                        "y": field_cords_y
                    },
                "type": type         
            }
        }
        broadcast(dart2Thrown)

    # Check for 3. Dart - Score-call
    elif turns != None and turns['throws'] != [] and len(turns['throws']) == 3:
        isGameFinished = False
        throwAmount = len(turns['throws'])
        type = turns['throws'][throwAmount - 1]['segment']['bed'].lower()
        field_name = turns['throws'][throwAmount - 1]['segment']['name'].lower()
        field_multiplier = turns['throws'][throwAmount - 1]['segment']['multiplier']
        field_number = turns['throws'][throwAmount - 1]['segment']['number']
        field_cords_x = turns['throws'][throwAmount - 1]['coords']['x']
        field_cords_y = turns['throws'][throwAmount - 1]['coords']['y']
        dart3score = str(int(points) - int(dart1score) - int(dart2score))
        dart3Thrown = {
            "event": "dart3-thrown",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "playerIsBot": str(currentPlayerIsBot),
            "game": {
                "mode": variant,
                "pointsLeft": str(remainingPlayerScore),
                "dartNumber": "3",
                "dartValue": dart3score,
                "fieldName": field_name,
                "fieldNumber": field_number,
                "fieldMultiplier": field_multiplier,
                "coords": {
                        "x": field_cords_x,
                        "y": field_cords_y
                    },
                "type": type         
            }
        }
        broadcast(dart3Thrown)
        dartsThrown = {
            "event": "darts-thrown",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "playerIsBot": str(currentPlayerIsBot),
            "game": {
                "mode": variant,
                "pointsLeft": str(remainingPlayerScore),
                "dartNumber": "3",
                "dartValue": points,        
            }
        }
        broadcast(dartsThrown)

        # BLIND SUPPORT: Announce total score after 3rd dart
        if CALL_BLIND_SUPPORT == 1:
            if currentPlayerIsBot == False:
                # Human player: announce total score
                blindSupport.announce_turn_total(turns['points'])
            elif currentPlayerIsBot:
                # Bot: only announce total score
                play_sound_effect(points, wait_for_last=True)
        elif currentPlayerIsBot == False or CALL_BOT_ACTIONS:
            # Normal mode: announce total score if conditions are met
            if CALL_EVERY_DART == 0 or CALL_EVERY_DART_TOTAL_SCORE == True:
                play_sound_effect(points, wait_for_last=CALL_EVERY_DART > 0)

            if AMBIENT_SOUNDS != 0.0:
                ambient_x_success = False

                throw_combo = ''
                for t in turns['throws']:
                    throw_combo += t['segment']['name'].lower()
                # ppi(throw_combo)

                if turns['points'] != 0:
                    ambient_x_success = play_sound_effect('ambient_' + str(throw_combo), AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    if ambient_x_success == False:
                        ambient_x_success = play_sound_effect('ambient_' + str(turns['points']), AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

                if ambient_x_success == False:
                    if turns['points'] >= 150:
                        play_sound_effect('ambient_150more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)   
                    elif turns['points'] >= 120:
                        play_sound_effect('ambient_120more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    elif turns['points'] >= 100:
                        play_sound_effect('ambient_100more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    elif turns['points'] >= 50:
                        play_sound_effect('ambient_50more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    elif turns['points'] >= 1:
                        play_sound_effect('ambient_1more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    else:
                        play_sound_effect('ambient_noscore', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

                # Koordinaten der Pfeile
                coords = []
                for t in turns['throws']:
                    if 'coords' in t:
                        coords.append({"x": t['coords']['x'], "y": t['coords']['y']})

                # ppi(str(coords))

                # Suche das Koordinatenpaar, das am weitesten von den beiden Anderen entfernt ist
                if len(coords) == 3:
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
                        play_sound_effect('ambient_group_legendary', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)   
                    elif group_score >= 95:
                        play_sound_effect('ambient_group_perfect', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    elif group_score >= 92:
                        play_sound_effect('ambient_group_very_nice', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    elif group_score >= 89:
                        play_sound_effect('ambient_group_good', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    elif group_score >= 86:
                        play_sound_effect('ambient_group_normal', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
     
        ppi("Turn ended")

    mirror_sounds()

    if isGameFin == True:
        isGameFinished = True

def process_match_cricket(m):
    global indexNameMacro
    currentPlayerIndex = m['player']
    currentPlayer = m['players'][currentPlayerIndex]
    currentPlayerName = str(currentPlayer['name']).lower()
    currentPlayerIsBot = (m['players'][currentPlayerIndex]['cpuPPR'] is not None)
    turns = m['turns'][0]
    variant = m['variant']
    gameMode = m['settings']['gameMode']

    isGameOn = False
    isGameFin = False
    global isGameFinished
    global lastPoints
    global dart1score
    global dart2score
    global dart3score

    # Call every thrown dart
    if CALL_EVERY_DART > 0 and turns != None and turns['throws'] != [] and len(turns['throws']) >= 1: 

        if currentPlayerIsBot == False or CALL_BOT_ACTIONS:

            throwAmount = len(turns['throws'])
            type = turns['throws'][throwAmount - 1]['segment']['bed'].lower()
            field_name = turns['throws'][throwAmount - 1]['segment']['name'].lower()
            field_number = turns['throws'][throwAmount - 1]['segment']['number']
            field_multiplier = turns['throws'][throwAmount - 1]['segment']['multiplier']
            if gameMode == 'Cricket':
                if field_number not in SUPPORTED_CRICKET_FIELDS:
                    return
            elif gameMode == 'Tactics':
                if field_number not in SUPPORTED_TACTICS_FIELDS:
                    return
            

            # TODO fields already closed?


            # SINGLE-DART-SCORE
            if CALL_EVERY_DART == 1:
                score = field_number * field_multiplier
                play_sound_effect(str(score))

            # SINGLE-DART-NAME
            elif CALL_EVERY_DART == 2:
                if field_number == 25 and field_multiplier == 1:
                    field_name = 'bull'
                elif field_number == 25 and field_multiplier == 2:
                    field_name = 'bullseye'

                # bull
                # bullseye 
                # s1 to t20
                # m1 to m20
                if play_sound_effect(field_name) == False:
                    field_number = str(field_number)

                    if type == 'singleouter' or type == 'singleinner':
                        play_sound_effect(field_number)
                    elif type == 'outside':
                        play_sound_effect(type)
                    else:
                        if play_sound_effect(type):
                            play_sound_effect(field_number, wait_for_last=True)

            # SINGLE-DART-EFFECT
            elif CALL_EVERY_DART == 3:
                if field_number == 25 and field_multiplier == 1:
                    field_name = 'bull'
                elif field_number == 25 and field_multiplier == 2:
                    field_name = 'bullseye'

                # effect_bull
                # effect_bullseye 
                # effect_s1 to effect_t20
                # effect_m1 to effect_m20
                if play_sound_effect('effect_' + field_name, mod = False) == False:

                    # effect_single
                    # effect_singleouter
                    # effect_singleinner
                    inner_outer = False
                    if type == 'singleouter' or type == 'singleinner':
                        inner_outer = play_sound_effect('effect_' + type, mod = False)
                        if inner_outer == False:
                            play_sound_effect('effect_single', mod = False)

                    # effect_double
                    # effect_triple 
                    # effect_outside
                    else:
                        play_sound_effect('effect_' + type, mod = False)


    # Check for matchshot
    if m['winner'] != -1 and isGameFinished == False:
        isGameFin = True

        throwPoints = 0
        lastPoints = ''
        for t in turns['throws']:
            number = t['segment']['number']
            if number in SUPPORTED_CRICKET_FIELDS or number in SUPPORTED_TACTICS_FIELDS:
                throwPoints += (t['segment']['multiplier'] * number)
                lastPoints += 'x' + str(t['segment']['name'])
        lastPoints = lastPoints[1:]
        
        matchWon = {
                "event": "match-won",
                "player": currentPlayerName,
                "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
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
            if play_sound_effect('ambient_matchshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            elif play_sound_effect('ambient_matchshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            elif play_sound_effect('ambient_gameshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            else:
                play_sound_effect('ambient_gameshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
        
        setup_caller()
        ppi('Gameshot and match')

    # Check for gameshot
    elif m['gameWinner'] != -1 and isGameFinished == False:
        isGameFin = True

        throwPoints = 0
        lastPoints = ''
        for t in turns['throws']:
            number = t['segment']['number']
            if number in SUPPORTED_CRICKET_FIELDS or number in SUPPORTED_CRICKET_FIELDS:
                throwPoints += (t['segment']['multiplier'] * number)
                lastPoints += 'x' + str(t['segment']['name'])
        lastPoints = lastPoints[1:]
        
        gameWon = {
                "event": "game-won",
                "player": currentPlayerName,
                "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
                "game": {
                    "mode": variant,
                    "dartsThrownValue": throwPoints
                } 
            }
        broadcast(gameWon)

        play_sound_effect('gameshot')
        play_sound_effect(currentPlayerName, True)
        
        if AMBIENT_SOUNDS != 0.0:
            if play_sound_effect('ambient_gameshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            else:
                play_sound_effect('ambient_gameshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
        
        if RANDOM_CALLER == 2:
            setup_caller()
        ppi('Gameshot')
    
    # Check for matchon
    elif m['gameScores'][0] == 0 and m['scores'] == None and turns['throws'] == [] and m['round'] == 1 and m['leg'] == 1 and m['set'] == 1:
        isGameOn = True
        isGameFinished = False

        matchStarted = {
            "event": "match-started",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
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
        # if AMBIENT_SOUNDS != 0.0 and ('legs' in m and 'sets'):
        #     if play_sound_effect('ambient_matchon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS) == False:
        #         play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)
        if AMBIENT_SOUNDS != 0.0:
            state = play_sound_effect('ambient_matchon_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
            if state == False and play_sound_effect('ambient_matchon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                if play_sound_effect('ambient_gameon_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                    play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)    
        
        ppi('Matchon')

    # Check for gameon
    elif m['gameScores'][0] == 0 and m['scores'] == None and turns['throws'] == [] and m['round'] == 1:
        isGameOn = True
        isGameFinished = False
        
        gameStarted = {
            "event": "game-started",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
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
            if play_sound_effect('ambient_gameon_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

        ppi('Gameon')

    # Check for busted turn
    elif turns['busted'] == True:
        lastPoints = "B"
        isGameFinished = False
        busted = { 
                    "event": "busted",
                    "player": currentPlayerName,
                    "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
                    "playerIsBot": str(currentPlayerIsBot),
                    "game": {
                        "mode": variant
                    }       
                }
        broadcast(busted)

        if currentPlayerIsBot == False or CALL_BOT_ACTIONS:
            play_sound_effect('busted')
            if AMBIENT_SOUNDS != 0.0:
                play_sound_effect('ambient_noscore', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
            ppi('Busted')

    # Check for 1. Dart
    elif turns != None and turns['throws'] != [] and len(turns['throws']) == 1:
        isGameFinished = False

    # Check for 2. Dart
    elif turns != None and turns['throws'] != [] and len(turns['throws']) == 2:
        isGameFinished = False

    # Check for 3. Dart - points call
    elif turns != None and turns['throws'] != [] and len(turns['throws']) == 3:
        isGameFinished = False

        # TODO fields already closed?
        throwPoints = 0
        lastPoints = ''
        for t in turns['throws']:
            number = t['segment']['number']
            if number in SUPPORTED_CRICKET_FIELDS or number in SUPPORTED_TACTICS_FIELDS:
                throwPoints += (t['segment']['multiplier'] * number)
                lastPoints += 'x' + str(t['segment']['name'])
        lastPoints = lastPoints[1:]

        dartsThrown = {
            "event": "darts-thrown",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "playerIsBot": str(currentPlayerIsBot),
            "game": {
                "mode": variant,
                "dartNumber": "3",
                "dartValue": throwPoints,        

            }
        }
        broadcast(dartsThrown)

        if currentPlayerIsBot == False or CALL_BOT_ACTIONS:
            if CALL_EVERY_DART == 0 or CALL_EVERY_DART_TOTAL_SCORE == True:
                play_sound_effect(str(throwPoints), wait_for_last=CALL_EVERY_DART != 0)

            if AMBIENT_SOUNDS != 0.0:
                if throwPoints == 0:
                    play_sound_effect('ambient_noscore', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                elif throwPoints == 180:
                    play_sound_effect('ambient_180', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                elif throwPoints >= 153:
                    play_sound_effect('ambient_150more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)   
                elif throwPoints >= 120:
                    play_sound_effect('ambient_120more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                elif throwPoints >= 100:
                    play_sound_effect('ambient_100more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                elif throwPoints >= 50:
                    play_sound_effect('ambient_50more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

        ppi("Turn ended")
    

    # Playerchange
    if isGameOn == False and turns != None and turns['throws'] == [] or isGameFinished == True:
        dartsPulled = {
            "event": "darts-pulled",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
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

        if currentPlayerIsBot == False or CALL_BOT_ACTIONS:
            if CALL_CURRENT_PLAYER == 2:
                play_sound_effect(currentPlayerName)

        if AMBIENT_SOUNDS != 0.0:
            if play_sound_effect('ambient_playerchange_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                play_sound_effect('ambient_playerchange', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
        
        ppi("Next player")

    mirror_sounds()

    if isGameFin == True:
        isGameFinished = True

def process_match_atc(m):
    global isGameFinished
    global indexNameMacro
    global blindSupport

    variant = m['variant']
    needHits = m['settings']['hits']
    currentPlayerIndex = m['player']
    currentPlayer = m['players'][currentPlayerIndex]
    currentPlayerName = str(currentPlayer['name']).lower()
    currentPlayerIsBot = (m['players'][currentPlayerIndex]['cpuPPR'] is not None)
    numberOfPlayers = len(m['players'])
    isRandomOrder = m['settings']['order'] == 'Random-Bull'
    isGameOn = False
    turns = m['turns'][0]
    matchshot = (m['winner'] != -1 and isGameFinished == False)

    currentTargetsPlayer = m['state']['currentTargets'][currentPlayerIndex]
    currentTarget = m['state']['targets'][currentPlayerIndex][int(currentTargetsPlayer)]

    # weird behavior by the api i guess?
    if currentTarget['count'] == 0 and int(currentTargetsPlayer) > 0 and turns['throws'] != []:
        currentTarget = m['state']['targets'][currentPlayerIndex][int(currentTargetsPlayer) -1]

    # BLIND SUPPORT: Announce target at turn start
    if turns['throws'] == []:
        blindSupport.announce_turn_start('ATC', m)

    if turns is not None and turns['throws']:
        isGameFinished = False
        
        # BLIND SUPPORT: Announce dart position
        lastThrow = turns['throws'][-1]
        blindSupport.announce_dart_result('ATC', lastThrow)

        # Only play normal ATC calls if blind support is disabled
        if (currentPlayerIsBot == False or CALL_BOT_ACTIONS) and CALL_BLIND_SUPPORT == 0:
            targetHit = lastThrow['segment']['number']

            hit = lastThrow['segment']['bed']
            target = currentTarget['bed']

            # ppi('hit: ' + hit + ' target: ' + target)
            is_correct_bed = False
            if hit != 'Outside' and target == 'Full':
                is_correct_bed = True
            elif hit == 'SingleInner' and (target == 'Inner Single' or target == 'Single'):
                is_correct_bed = True
            elif hit == 'SingleOuter' and (target == 'Outer Single' or target == 'Single'):
                is_correct_bed = True
            elif hit == 'Double' and target == 'Double':
                is_correct_bed = True
            elif hit == 'Triple' and target == 'Triple':
                is_correct_bed = True

            if targetHit == currentTarget['number'] and is_correct_bed:
                if play_sound_effect('atc_target_hit') == False:
                    play_sound_effect(str(targetHit))
            else:
                if play_sound_effect('atc_target_missed') == False:
                    play_sound_effect(str(targetHit))
    # Check for matchon
    # elif turns['throws'] == [] and m['round'] == 1 and m['leg'] == 1 and m['set'] == 1:
    #     isGameOn = True
    #     isGameFinished = False

    #     matchStarted = {
    #         "event": "match-started",
    #         "player": currentPlayerName,
    #         "playerIndex": str(currentPlayerIndex),
    #         "game": {
    #             "mode": variant,
    #             # TODO: fix
    #             "special": "TODO"
    #             }     
    #         }
    #     broadcast(matchStarted)

    #     play_sound_effect(currentPlayerName, False)
    #     if play_sound_effect('matchon', True) == False:
    #         play_sound_effect('gameon', True)
        
    #     # play only if it is a real match not just legs!
    #     # if AMBIENT_SOUNDS != 0.0 and ('legs' in m and 'sets'):
    #     #     if play_sound_effect('ambient_matchon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS) == False:
    #     #         play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)
    #     if AMBIENT_SOUNDS != 0.0:
    #         state = play_sound_effect('ambient_matchon_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
    #         if state == False and play_sound_effect('ambient_matchon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
    #             if play_sound_effect('ambient_gameon_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
    #                 play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)    
        
    #     ppi('Matchon')

    # # Check for gameon
    # elif turns['throws'] == [] and m['round'] == 1:
    #     isGameOn = True
    #     isGameFinished = False
        
    #     gameStarted = {
    #         "event": "game-started",
    #         "player": currentPlayerName,
    #         "playerIndex": str(currentPlayerIndex),
    #         "game": {
    #             "mode": variant,
    #             # TODO: fix
    #             "special": "TODO"
    #             }     
    #         }
    #     broadcast(gameStarted)

    #     play_sound_effect(currentPlayerName, False)
    #     play_sound_effect('gameon', True)

    #     if AMBIENT_SOUNDS != 0.0:
    #         if play_sound_effect('ambient_gameon_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
    #             play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

    #     ppi('Gameon')

    if matchshot:
        isGameFinished = True
        matchWon = {
            "event": "match-won",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "game": {
                "mode": variant,
                "dartsThrownValue": "0"
            } 
        }
        broadcast(matchWon)

        if play_sound_effect('matchshot') == False:
            play_sound_effect('gameshot')

        if CALL_CURRENT_PLAYER >= 1:
            play_sound_effect(currentPlayerName, True)

        if AMBIENT_SOUNDS != 0.0:
            if play_sound_effect('ambient_matchshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            elif play_sound_effect('ambient_matchshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            elif play_sound_effect('ambient_gameshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            else:
                play_sound_effect('ambient_gameshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

        ppi('Gameshot and match')

    # only call next if more hits then 1
    elif currentTarget['hits'] == needHits and turns['throws'] != [] and (needHits > 1 or isRandomOrder):

        if currentPlayerIsBot == False or CALL_BOT_ACTIONS:
            play_sound_effect('atc_target_next', True)
            # only call next target number if random order
            if isRandomOrder:
                play_sound_effect(str(m['state']['targets'][currentPlayerIndex][int(currentTargetsPlayer)]['number']), True)


    if turns['throws'] == []:
        if AMBIENT_SOUNDS != 0.0:
            if play_sound_effect('ambient_playerchange_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                play_sound_effect('ambient_playerchange', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

        if currentPlayerIsBot == False or CALL_BOT_ACTIONS:
            if CALL_CURRENT_PLAYER == 2 and numberOfPlayers > 1:
                play_sound_effect(currentPlayerName, True)

    # Playerchange
    if turns != None and turns['throws'] == [] or isGameFinished == True:
        dartsPulled = {
            "event": "darts-pulled",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "game": {
                "mode": variant
            }
        }
        broadcast(dartsPulled)

        if currentPlayerIsBot == False or CALL_BOT_ACTIONS:
            if CALL_CURRENT_PLAYER == 2:
                play_sound_effect(currentPlayerName)

        if AMBIENT_SOUNDS != 0.0:
            if play_sound_effect('ambient_playerchange_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                play_sound_effect('ambient_playerchange', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
        
        ppi("Next player")
    
    mirror_sounds()

def process_match_rtw(m):
    global indexNameMacro
    global isGameFinished
    global blindSupport

    variant = m['variant']
    currentPlayerIndex = m['player']
    currentPlayerName = m['players'][currentPlayerIndex]['name'].lower()
    currentPlayerIsBot = (m['players'][currentPlayerIndex]['cpuPPR'] is not None)
    numberOfPlayers = len(m['players'])
    isRandomOrder = m['settings']['order'] == 'Random-Bull'
    winningPlayerIndex = int(m['winner'])
    winningPlayerName = ''
    if winningPlayerIndex != -1:
        winningPlayerName = m['players'][winningPlayerIndex]['name'].lower()
    order = m['settings']['order']
    turn = m['turns'][0]
    points = turn['points']
    currentTarget = 0
    if order == '1-20-Bull':
        currentTarget = m['round']
    elif order == '20-1-Bull':
        currentTarget = 21 - m['round']
    if currentTarget == 0 or currentTarget == 21:
        currentTarget = 25

    gameon = (0 == m['gameScores'][0] and turn['throws'] == [])
    matchover = (winningPlayerIndex != -1 and isGameFinished == False)
    
    # BLIND SUPPORT: Announce target at turn start
    if turn['throws'] == []:
        blindSupport.announce_turn_start('RTW', m)
    
    if turn is not None and turn['throws']:
        isGameFinished = False
        
        # BLIND SUPPORT: Announce dart position
        lastThrow = turn['throws'][-1]
        blindSupport.announce_dart_result('RTW', lastThrow)


    # Darts pulled (Playerchange and Possible-checkout)
    if gameon == False and turn != None and turn['throws'] == [] or isGameFinished == True:
        dartsPulled = {
            "event": "darts-pulled",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "game": {
                "mode": variant,
                # TODO: fix
                "dartsThrown": "3",
                "dartsThrownValue": points,
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

    elif CALL_EVERY_DART > 0 and turn is not None and turn['throws'] and not isRandomOrder and CALL_BLIND_SUPPORT == 0:

        if currentPlayerIsBot == False or CALL_BOT_ACTIONS:
            lastThrow = turn['throws'][-1]
            targetHit = lastThrow['segment']['number']

            hit = lastThrow['segment']['bed']

            if targetHit == currentTarget:
                if hit == 'Single' or hit == 'SingleInner' or hit == 'SingleOuter':
                    if play_sound_effect('rtw_target_hit_single', True, mod = False) == False:
                        if play_sound_effect(hit, wait_for_last = True, mod = False) == False:
                            play_sound_effect(str(1), wait_for_last = True, mod = True)
                elif hit == 'Double':
                    if play_sound_effect('rtw_target_hit_double', wait_for_last = True, mod = False) == False:
                        if play_sound_effect(hit, wait_for_last = True, mod = False) == False:
                            play_sound_effect(str(2), wait_for_last = True, mod = True)
                elif hit == 'Triple':
                    if play_sound_effect('rtw_target_hit_triple', wait_for_last = True, mod = False) == False:
                        if play_sound_effect(hit, wait_for_last = True, mod = False) == False:
                            play_sound_effect(str(3), wait_for_last = True, mod = True)
            else:
                if play_sound_effect('rtw_target_missed', wait_for_last = True, mod = False) == False:
                    play_sound_effect(str(0), wait_for_last = True, mod = True)


    # Check for 3. Dart - points call
    if turn != None and turn['throws'] != [] and len(turn['throws']) == 3:
        dartsThrown = {
            "event": "darts-thrown",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "playerIsBot": str(currentPlayerIsBot),
            "game": {
                "mode": variant,
                "dartNumber": "3",
                "dartValue": points,        

            }
        }
        broadcast(dartsThrown)

        if currentPlayerIsBot == False or CALL_BOT_ACTIONS:
            play_sound_effect(str(points), True)
            if AMBIENT_SOUNDS != 0.0:
                if int(points) == 0:
                    play_sound_effect('ambient_noscore', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                elif int(points) == 9:
                    play_sound_effect('ambient_180', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                elif int(points) >= 7:
                    play_sound_effect('ambient_150more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)   
                elif int(points) >= 6:
                    play_sound_effect('ambient_120more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                elif int(points) >= 5:
                    play_sound_effect('ambient_100more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                elif int(points) >= 4:
                    play_sound_effect('ambient_50more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

        ppi("Turn ended")
    

    if matchover:
        isGameFinished = True
        matchWon = {
            "event": "match-won",
            "player": m['players'][winningPlayerIndex],
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "game": {
                "mode": variant,
                "dartsThrownValue": "0"
            } 
        }
        broadcast(matchWon)

        if play_sound_effect('matchshot') == False:
            play_sound_effect('gameshot')

        if CALL_CURRENT_PLAYER >= 1:
            play_sound_effect(winningPlayerName, True)

        if AMBIENT_SOUNDS != 0.0:
            if play_sound_effect('ambient_matchshot_' + winningPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            elif play_sound_effect('ambient_matchshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            elif play_sound_effect('ambient_gameshot_' + winningPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            else:
                play_sound_effect('ambient_gameshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

        ppi('Gameshot and match')
        

    if m['gameScores'][0] == 0 and m['scores'] == None and turn['throws'] == [] and m['round'] == 1:
        isGameOn = True
        isGameFinished = False
        
        gameStarted = {
            "event": "game-started",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
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
            if play_sound_effect('ambient_gameon_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

        ppi('Gameon')

    # only call next target number if random order
    if isRandomOrder:
        if currentPlayerIsBot == False or CALL_BOT_ACTIONS:
            # [int(currentTargetsPlayer)] REMOVE?!
            play_sound_effect(str(m['state']['targets'][currentPlayerIndex]['number']), True)


    if turn['throws'] == []:
        if AMBIENT_SOUNDS != 0.0:
            if play_sound_effect('ambient_playerchange_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                play_sound_effect('ambient_playerchange', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

        if currentPlayerIsBot == False or CALL_BOT_ACTIONS:
            if CALL_CURRENT_PLAYER == 2 and numberOfPlayers > 1:
                play_sound_effect(currentPlayerName, True)
    # Playerchange
    if turn != None and turn['throws'] == [] or isGameFinished == True:
        dartsPulled = {
            "event": "darts-pulled",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "game": {
                "mode": variant
            }
        }
        broadcast(dartsPulled)

        if currentPlayerIsBot == False or CALL_BOT_ACTIONS:
            if CALL_CURRENT_PLAYER == 2:
                play_sound_effect(currentPlayerName)

        if AMBIENT_SOUNDS != 0.0:
            if play_sound_effect('ambient_playerchange_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                play_sound_effect('ambient_playerchange', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
        
        ppi("Next player")
    mirror_sounds()

def process_bulling(m):
    global indexNameMacro
    global isBullingFinished
    currentPlayerIndex = m['player']
    currentPlayer = m['players'][currentPlayerIndex]
    currentPlayerName = str(currentPlayer['name']).lower()
    currentPlayerIsBot = (m['players'][currentPlayerIndex]['cpuPPR'] is not None)
    gameshot = m['gameWinner'] != -1

    if gameshot == True:
        isBullingFinished = True
        bullingEnd = {
            "event": "bulling-end",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "playerIsBot": str(currentPlayerIsBot)
        }
        broadcast(bullingEnd)

        name = play_sound_effect((m['players'][m['gameWinner']]['name']).lower())
        if name:
            play_sound_effect('bulling_end', wait_for_last=True)
    else:
        if m['round'] == 1 and m['gameScores'] is None:  
            isBullingFinished = False
            bullingStart = {
                "event": "bulling-start",
                "player": currentPlayerName,
                "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
                "playerIsBot": str(currentPlayerIsBot)
            }
            broadcast(bullingStart)

            play_sound_effect('bulling_start')
        
    mirror_sounds()

def process_match_CountUp(m):
    global indexNameMacro
    global blindSupport
    currentPlayerIndex = m['player']
    currentPlayer = m['players'][currentPlayerIndex]
    currentPlayerName = str(currentPlayer['name']).lower()
    currentPlayerIsBot = (m['players'][currentPlayerIndex]['cpuPPR'] is not None)
    turns = m['turns'][0]
    variant = m['variant']

    isGameOn = False
    isGameFin = False
    global isGameFinished
    global lastPoints

    # Call every thrown dart
    if CALL_EVERY_DART > 0 and turns != None and turns['throws'] != [] and len(turns['throws']) >= 1: 

        # BLIND SUPPORT: Announce dart position
        if CALL_BLIND_SUPPORT == 1:
            lastThrow = turns['throws'][-1]
            blindSupport.announce_dart_result('CountUp', lastThrow)

        elif currentPlayerIsBot == False or CALL_BOT_ACTIONS:

            throwAmount = len(turns['throws'])
            type = turns['throws'][throwAmount - 1]['segment']['bed'].lower()
            field_name = turns['throws'][throwAmount - 1]['segment']['name'].lower()
            field_number = turns['throws'][throwAmount - 1]['segment']['number']
            field_multiplier = turns['throws'][throwAmount - 1]['segment']['multiplier']         

            # SINGLE-DART-SCORE
            if CALL_EVERY_DART == 1:
                score = field_number * field_multiplier
                play_sound_effect(str(score))

            # SINGLE-DART-NAME
            elif CALL_EVERY_DART == 2:
                if field_number == 25 and field_multiplier == 1:
                    field_name = 'bull'
                elif field_number == 25 and field_multiplier == 2:
                    field_name = 'bullseye'

                # bull
                # bullseye 
                # s1 to t20
                # m1 to m20
                if play_sound_effect(field_name) == False:
                    field_number = str(field_number)

                    if type == 'singleouter' or type == 'singleinner':
                        play_sound_effect(field_number)
                    elif type == 'outside':
                        play_sound_effect(type)
                    else:
                        if play_sound_effect(type):
                            play_sound_effect(field_number, wait_for_last=True)

            # SINGLE-DART-EFFECT
            elif CALL_EVERY_DART == 3:
                if field_number == 25 and field_multiplier == 1:
                    field_name = 'bull'
                elif field_number == 25 and field_multiplier == 2:
                    field_name = 'bullseye'

                # effect_bull
                # effect_bullseye 
                # effect_s1 to effect_t20
                # effect_m1 to effect_m20
                if play_sound_effect('effect_' + field_name, mod = False) == False:

                    # effect_single
                    # effect_singleouter
                    # effect_singleinner
                    inner_outer = False
                    if type == 'singleouter' or type == 'singleinner':
                        inner_outer = play_sound_effect('effect_' + type, mod = False)
                        if inner_outer == False:
                            play_sound_effect('effect_single', mod = False)

                    # effect_double
                    # effect_triple 
                    # effect_outside
                    else:
                        play_sound_effect('effect_' + type, mod = False)
    # Check for matchshot
    if m['winner'] != -1 and isGameFinished == False:
        isGameFin = True

        throwPoints = 0
        lastPoints = ''
        for t in turns['throws']:
            number = t['segment']['number']
            throwPoints += (t['segment']['multiplier'] * number)
            lastPoints += 'x' + str(t['segment']['name'])
        lastPoints = lastPoints[1:]
        
        matchWon = {
                "event": "match-won",
                "player": currentPlayerName,
                "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
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
            if play_sound_effect('ambient_matchshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            elif play_sound_effect('ambient_matchshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            elif play_sound_effect('ambient_gameshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            else:
                play_sound_effect('ambient_gameshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
        
        setup_caller()
        ppi('Gameshot and match')

    # Check for gameshot
    elif m['gameWinner'] != -1 and isGameFinished == False:
        isGameFin = True

        throwPoints = 0
        lastPoints = ''
        for t in turns['throws']:
            number = t['segment']['number']
            throwPoints += (t['segment']['multiplier'] * number)
            lastPoints += 'x' + str(t['segment']['name'])
        lastPoints = lastPoints[1:]
        
        gameWon = {
                "event": "game-won",
                "player": currentPlayerName,
                "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
                "game": {
                    "mode": variant,
                    "dartsThrownValue": throwPoints
                } 
            }
        broadcast(gameWon)

        play_sound_effect('gameshot')
        play_sound_effect(currentPlayerName, True)
        
        if AMBIENT_SOUNDS != 0.0:
            if play_sound_effect('ambient_gameshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            else:
                play_sound_effect('ambient_gameshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
        
        if RANDOM_CALLER == 2:
            setup_caller()
        ppi('Gameshot')
    
    # Check for matchon
    elif m['gameScores'][0] == 0 and m['scores'] == None and turns['throws'] == [] and m['round'] == 1 and m['leg'] == 1 and m['set'] == 1:
        isGameOn = True
        isGameFinished = False

        matchStarted = {
            "event": "match-started",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
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
        # if AMBIENT_SOUNDS != 0.0 and ('legs' in m and 'sets'):
        #     if play_sound_effect('ambient_matchon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS) == False:
        #         play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)
        if AMBIENT_SOUNDS != 0.0:
            state = play_sound_effect('ambient_matchon_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
            if state == False and play_sound_effect('ambient_matchon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                if play_sound_effect('ambient_gameon_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                    play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)    
        
        ppi('Matchon')

    # Check for gameon
    elif m['gameScores'][0] == 0 and m['scores'] == None and turns['throws'] == [] and m['round'] == 1:
        isGameOn = True
        isGameFinished = False
        
        gameStarted = {
            "event": "game-started",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
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
            if play_sound_effect('ambient_gameon_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

        ppi('Gameon')

        if currentPlayerIsBot == False or CALL_BOT_ACTIONS:
            play_sound_effect('busted')
            if AMBIENT_SOUNDS != 0.0:
                play_sound_effect('ambient_noscore', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
            ppi('Busted')

    # Check for 1. Dart
    elif turns != None and turns['throws'] != [] and len(turns['throws']) == 1:
        isGameFinished = False

    # Check for 2. Dart
    elif turns != None and turns['throws'] != [] and len(turns['throws']) == 2:
        isGameFinished = False

    # Check for 3. Dart - points call
    elif turns != None and turns['throws'] != [] and len(turns['throws']) == 3:
        isGameFinished = False

        # TODO fields already closed?
        throwPoints = 0
        lastPoints = ''
        for t in turns['throws']:
            number = t['segment']['number']
            throwPoints += (t['segment']['multiplier'] * number)
            lastPoints += 'x' + str(t['segment']['name'])
        lastPoints = lastPoints[1:]

        dartsThrown = {
            "event": "darts-thrown",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "playerIsBot": str(currentPlayerIsBot),
            "game": {
                "mode": variant,
                "dartNumber": "3",
                "dartValue": throwPoints,        

            }
        }
        broadcast(dartsThrown)

        if currentPlayerIsBot == False or CALL_BOT_ACTIONS:
            if CALL_EVERY_DART == 0 or CALL_EVERY_DART_TOTAL_SCORE == True:
                play_sound_effect(str(throwPoints), wait_for_last=CALL_EVERY_DART != 0)

            if AMBIENT_SOUNDS != 0.0:
                if throwPoints == 0:
                    play_sound_effect('ambient_noscore', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                elif throwPoints == 180:
                    play_sound_effect('ambient_180', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                elif throwPoints >= 153:
                    play_sound_effect('ambient_150more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)   
                elif throwPoints >= 120:
                    play_sound_effect('ambient_120more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                elif throwPoints >= 100:
                    play_sound_effect('ambient_100more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                elif throwPoints >= 50:
                    play_sound_effect('ambient_50more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

        ppi("Turn ended")
    

    # Playerchange
    if isGameOn == False and turns != None and turns['throws'] == [] or isGameFinished == True:
        dartsPulled = {
            "event": "darts-pulled",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "game": {
                "mode": variant,
                # TODO: fix
                "dartsThrown": "3",
                "dartsThrownValue": lastPoints,
                # TODO: fix
                # "darts": [
                #     {"number": "1", "value": "60"},
                #     {"number": "2", "value": "60"},
                #     {"number": "3", "value": "60"}
                # ]
            }
        }
        broadcast(dartsPulled)

        if currentPlayerIsBot == False or CALL_BOT_ACTIONS:
            if CALL_CURRENT_PLAYER == 2:
                play_sound_effect(currentPlayerName)

        if AMBIENT_SOUNDS != 0.0:
            if play_sound_effect('ambient_playerchange_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                play_sound_effect('ambient_playerchange', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
        
        ppi("Next player")

    mirror_sounds()

    if isGameFin == True:
        isGameFinished = True

def process_match_Bermuda(m):
    global indexNameMacro
    global BERMUDA_ROUNDS
    global currentMatch
    global currentMatchHost
    global currentMatchPlayers
    global isGameFinished
    global oneGoodDart
    global bermudaBusted
    global blindSupport
    
    variant = m['variant']
    players = m['players']
    currentPlayerIndex = m['player']
    currentPlayer = m['players'][currentPlayerIndex]
    currentPlayerName = str(currentPlayer['name']).lower()
    currentPlayerIsBot = (m['players'][currentPlayerIndex]['cpuPPR'] is not None)
    numberOfPlayers = len(m['players'])

    turns = m['turns'][0]
    points = str(turns['points'])


    rounds = m['round']
    target = BERMUDA_ROUNDS[rounds]
    throwAmount = len(turns['throws'])
    # type = turns['throws'][throwAmount - 1]['segment']['bed'].lower()
    # field_name = turns['throws'][throwAmount - 1]['segment']['name'].lower()
    # field_multiplier = turns['throws'][throwAmount - 1]['segment']['multiplier']
    # field_number = turns['throws'][throwAmount - 1]['segment']['number']
    pcc_success = False
    isGameFin = False

    # ppi('CurrentPlayerName: ' + currentPlayerName)
    # ppi('CurrentPlayerIsBot: ' + str(currentPlayerIsBot))
    # ppi('rounds: ' + str(rounds))
    # ppi('variant: ' + variant)
    # ppi('target: ' + target)
    # ppi('segment type: ' + type + ' Feld Name: ' + field_name + ' Feld Multiplikator: ' + str(field_multiplier) + ' Feld Nummer: ' + str(field_number))
    # ppi(json.dumps(m, indent = 4, sort_keys = True))
    matchshot = (m['winner'] != -1 and isGameFinished == False)
    gameshot = (m['gameWinner'] != -1 and isGameFinished == False)

    matchon = (turns['throws'] == [] and m['leg'] == 1 and m['set'] == 1 and rounds == 1)
    gameon = (turns['throws'] == [] and rounds == 1)
    
    # BLIND SUPPORT: Announce target at turn start
    if turns['throws'] == []:
        blindSupport.announce_turn_start('Bermuda', m)

    # CHECK FOR BUSTED TURN
    if turns != None and turns['throws'] == []:
        oneGoodDart = False
    if turns != None and turns['throws'] != []:
        field_name = turns['throws'][throwAmount - 1]['segment']['name'].lower()
        field_multiplier = turns['throws'][throwAmount - 1]['segment']['multiplier']
        field_number = turns['throws'][throwAmount - 1]['segment']['number']
        
        # BLIND SUPPORT: Announce dart position
        lastThrow = turns['throws'][-1]
        blindSupport.announce_dart_result('Bermuda', lastThrow)
        
        if str(field_number) == target:
            # ppi('hit: ' + str(field_number) + ' target: ' + str(target))
            oneGoodDart = True
            bermudaBusted = "False"
        elif field_multiplier == 3 and target =='T' :
            # ppi('hit: ' + str(field_name) + ' target: ' + str(target))
            oneGoodDart = True
            bermudaBusted = "False"
        elif field_multiplier == 2 and target =='D' :
            # ppi('hit: ' + str(field_name) + ' target: ' + str(target))
            oneGoodDart = True
            bermudaBusted = "False"
        elif field_multiplier == 2 and field_number == 25 and target =='50' :
            # ppi('hit: ' + str(field_name) + ' target: ' + str(target))
            oneGoodDart = True
            bermudaBusted = "False"
        elif oneGoodDart == False:
            # ppi('BUSTED')
            bermudaBusted = "True"
    

    # Darts pulled (Playerchange and Possible-checkout)
    if gameon == False and turns != None and turns['throws'] == [] or isGameFinished == True:
        dartsPulled = {
            "event": "darts-pulled",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "game": {
                "mode": variant,
                # TODO: fix
                "dartsThrown": "3",
                "round": str(rounds),
                "target": BERMUDA_ROUNDS[rounds],
                "busted": bermudaBusted
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

            if currentPlayerIsBot == False or CALL_BOT_ACTIONS:

                if pcc_success == False and CALL_CURRENT_PLAYER == 2 and numberOfPlayers > 1:
                    play_sound_effect(currentPlayerName)

            # Player-change
            if pcc_success == False and AMBIENT_SOUNDS != 0.0:
                if play_sound_effect('ambient_playerchange_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                    play_sound_effect('ambient_playerchange', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                

            ppi("Next player")
    
    elif CALL_EVERY_DART > 0 and turns != None and turns['throws'] != [] and len(turns['throws']) >= 1 and matchshot == False and gameshot == False: 
        
        if currentPlayerIsBot == False or CALL_BOT_ACTIONS:
            throwAmount = len(turns['throws'])
            type = turns['throws'][throwAmount - 1]['segment']['bed'].lower()
            field_name = turns['throws'][throwAmount - 1]['segment']['name'].lower()
            field_multiplier = turns['throws'][throwAmount - 1]['segment']['multiplier']
            field_number = turns['throws'][throwAmount - 1]['segment']['number']
            # ppi("Type: " + str(type) + " - Field-name: " + str(field_name))
            # ppi(turns['throws'][throwAmount - 1]['segment'])
                

            # SINGLE-DART-SCORE
            if CALL_EVERY_DART == 1:
                score = field_number * field_multiplier
                play_sound_effect(str(score))

            # SINGLE-DART-NAME
            elif CALL_EVERY_DART == 2:
                if field_number == 25 and field_multiplier == 1:
                    field_name = 'bull'
                elif field_number == 25 and field_multiplier == 2:
                    field_name = 'bullseye'

                # bull
                # bullseye 
                # s1 to t20
                # m1 to m20
                if play_sound_effect(field_name) == False:
                    field_number = str(field_number)

                    if type == 'singleouter' or type == 'singleinner':
                        play_sound_effect(field_number)
                    elif type == 'outside':
                        play_sound_effect(type)
                    else:
                        if play_sound_effect(type):
                            play_sound_effect(field_number, wait_for_last=True)

            # SINGLE-DART-EFFECT
            elif CALL_EVERY_DART == 3:
                if field_number == 25 and field_multiplier == 1:
                    field_name = 'bull'
                elif field_number == 25 and field_multiplier == 2:
                    field_name = 'bullseye'

                # effect_bull
                # effect_bullseye 
                # effect_s1 to effect_t20
                # effect_m1 to effect_m20
                if play_sound_effect('effect_' + field_name, mod = False) == False:

                    # effect_single
                    # effect_singleouter
                    # effect_singleinner
                    inner_outer = False
                    if type == 'singleouter' or type == 'singleinner':
                        inner_outer = play_sound_effect('effect_' + type, mod = False)
                        if inner_outer == False:
                            play_sound_effect('effect_single', mod = False)

                    # effect_double
                    # effect_triple 
                    # effect_outside
                    else:
                        play_sound_effect('effect_' + type, mod = False)
    # Check for matchshot
    if matchshot == True:
        isGameFin = True
        
        matchWon = {
                "event": "match-won",
                "player": currentPlayerName,
                "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
                "game": {
                    "mode": variant,
                    "dartsThrownValue": points
                } 
            }
        broadcast(matchWon)

        if play_sound_effect('matchshot') == False:
            play_sound_effect('gameshot')

        if CALL_CURRENT_PLAYER >= 1:
            play_sound_effect(currentPlayerName, True)

        if AMBIENT_SOUNDS != 0.0:
            if play_sound_effect('ambient_matchshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            elif play_sound_effect('ambient_matchshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            elif play_sound_effect('ambient_gameshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            else:
                play_sound_effect('ambient_gameshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
            

        if RANDOM_CALLER == 2:
            setup_caller()
        ppi('Gameshot and match')

    # Check for gameshot
    elif gameshot == True:
        isGameFin = True
        
        gameWon = {
                "event": "game-won",
                "player": currentPlayerName,
                "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
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
        # maxLeg = m['legs']
        # maxSets = m['sets']

        # ppi('currentLeg: ' + str(currentLeg))
        # ppi('currentSet: ' + str(currentSet))

        isSet = False
        if 'sets' not in m:
            play_sound_effect('leg_' + str(currentLeg), gameshotState)
        else:
            if currentPlayerScoreLegs == 0:
                play_sound_effect('set_' + str(currentSet), gameshotState)
                isSet = True
            else:
                play_sound_effect('leg_' + str(currentLeg), gameshotState)    

        if CALL_CURRENT_PLAYER >= 1:
            play_sound_effect(currentPlayerName, True)

        if AMBIENT_SOUNDS != 0.0:
            if isSet == True:
                if play_sound_effect('ambient_setshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                    pass
                elif play_sound_effect('ambient_setshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                    pass
                elif play_sound_effect('ambient_gameshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                    pass
                else:
                    play_sound_effect('ambient_gameshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    
            else:
                if play_sound_effect('ambient_gameshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                    pass
                else:
                    play_sound_effect('ambient_gameshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

        if RANDOM_CALLER == 2:
            setup_caller()
        ppi('Gameshot')        

    # Check for matchon
    elif matchon == True:
        isGameFinished = False

        currentMatchPlayers = []
        currentMatchHost = None
        if players != []:
            for p in players:
                if 'boardId' in p:
                    if currentMatchHost is None and m['host']['id'] == p['userId'] and p['boardId'] == AUTODART_USER_BOARD_ID:
                        currentMatchHost = True
                    else:
                        currentMatchPlayers.append(p)

        matchStarted = {
            "event": "match-started",
            "id": currentMatch,
            "me": AUTODART_USER_BOARD_ID,
            # "meHost": currentMatchHost,
            # "players": currentMatchPlayers,
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "game": {
                "mode": variant,
                # TODO: fix
                "special": "TODO"
                }     
            }
        broadcast(matchStarted)

        callPlayerNameState = False
        if CALL_CURRENT_PLAYER >= 1:
            callPlayerNameState = play_sound_effect(currentPlayerName)

        if play_sound_effect('matchon', callPlayerNameState, mod = False) == False:
            play_sound_effect('gameon', callPlayerNameState, mod = False)

        if AMBIENT_SOUNDS != 0.0:
            state = play_sound_effect('ambient_matchon_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
            if state == False and play_sound_effect('ambient_matchon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                if play_sound_effect('ambient_gameon_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                    play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)


        ppi('Matchon')

    # Check for gameon
    elif gameon == True:
        isGameFinished = False

        gameStarted = {
            "event": "game-started",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "game": {
                "mode": variant,
                # TODO: fix
                "special": "TODO"
                }     
            }
        broadcast(gameStarted)

        callPlayerNameState = False
        if CALL_CURRENT_PLAYER >= 1:
            callPlayerNameState = play_sound_effect(currentPlayerName)

        play_sound_effect('gameon', callPlayerNameState, mod = False)

        if AMBIENT_SOUNDS != 0.0:
            if play_sound_effect('ambient_gameon_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

        ppi('Gameon')

    # Check for 1. Dart
    elif turns != None and turns['throws'] != [] and len(turns['throws']) == 1:
        isGameFinished = False
        dart1Thrown = {
            "event": "dart1-thrown",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "playerIsBot": str(currentPlayerIsBot),
            "game": {
                "mode": variant,
                "dartNumber": "1",
                "dartValue": points,
                "round": str(rounds),
                "target": BERMUDA_ROUNDS[rounds]      
            }
        }
        broadcast(dart1Thrown)

    # Check for 2. Dart
    elif turns != None and turns['throws'] != [] and len(turns['throws']) == 2:
        isGameFinished = False
        dart2Thrown = {
            "event": "dart2-thrown",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "playerIsBot": str(currentPlayerIsBot),
            "game": {
                "mode": variant,
                "dartNumber": "2",
                "round": str(rounds),
                "target": BERMUDA_ROUNDS[rounds]      
            }
        }
        broadcast(dart2Thrown)

    # Check for 3. Dart - Score-call
    elif turns != None and turns['throws'] != [] and len(turns['throws']) == 3:
        isGameFinished = False
        # dart3score = str(int(points) - int(dart1score) - int(dart2score))
        dart3Thrown = {
            "event": "dart3-thrown",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "playerIsBot": str(currentPlayerIsBot),
            "game": {
                "mode": variant,
                "dartNumber": "3",
                "round": str(rounds),
                "target": BERMUDA_ROUNDS[rounds]      
            }
        }
        broadcast(dart3Thrown)
        dartsThrown = {
            "event": "darts-thrown",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "playerIsBot": str(currentPlayerIsBot),
            "game": {
                "mode": variant,
                "dartNumber": "3",
                "dartValue": points,
                "round": str(rounds),
                "target": BERMUDA_ROUNDS[rounds]      
            }
        }
        # ppi(dartsThrown)
        broadcast(dartsThrown)

        if currentPlayerIsBot == False or CALL_BOT_ACTIONS:
            if CALL_EVERY_DART == 0 or CALL_EVERY_DART_TOTAL_SCORE == True:
                if int(points) <= 0:
                    points = str(int(points) * -1)
                    minuspoints = play_sound_effect("ber_minus", wait_for_last=CALL_EVERY_DART > 0)
                    if minuspoints == False:
                        points = "0"
                play_sound_effect(points, wait_for_last=CALL_EVERY_DART > 0)

            if bermudaBusted == "True":
                busted = { 
                "event": "busted",
                "player": currentPlayerName,
                "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
                "playerIsBot": str(currentPlayerIsBot),
                "game": {
                    "mode": variant
                    }       
                }
                broadcast(busted)
                ppi('Busted')
                bermudaBusted = "False"

            if AMBIENT_SOUNDS != 0.0:
                ambient_x_success = False

                
                if ambient_x_success == False:
                    if turns['points'] >= 150:
                        play_sound_effect('ambient_150more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)   
                    elif turns['points'] >= 120:
                        play_sound_effect('ambient_120more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    elif turns['points'] >= 100:
                        play_sound_effect('ambient_100more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    elif turns['points'] >= 50:
                        play_sound_effect('ambient_50more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    elif turns['points'] >= 1:
                        play_sound_effect('ambient_1more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    else:
                        play_sound_effect('ambient_noscore', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

                # Koordinaten der Pfeile
                coords = []
                for t in turns['throws']:
                    if 'coords' in t:
                        coords.append({"x": t['coords']['x'], "y": t['coords']['y']})

                # ppi(str(coords))

                # Suche das Koordinatenpaar, das am weitesten von den beiden Anderen entfernt ist
                if len(coords) == 3:
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
                        play_sound_effect('ambient_group_legendary', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)   
                    elif group_score >= 95:
                        play_sound_effect('ambient_group_perfect', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    elif group_score >= 92:
                        play_sound_effect('ambient_group_very_nice', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    elif group_score >= 89:
                        play_sound_effect('ambient_group_good', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    elif group_score >= 86:
                        play_sound_effect('ambient_group_normal', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
     
        ppi("Turn ended")

    mirror_sounds()

    if isGameFin == True:
        isGameFinished = True

def process_match_shanghai(m):
    global indexNameMacro
    global currentMatch
    global currentMatchHost
    global currentMatchPlayers
    global isGameFinished
    global blindSupport
    
    variant = m['variant']
    players = m['players']
    currentPlayerIndex = m['player']
    currentPlayer = m['players'][currentPlayerIndex]
    currentPlayerName = str(currentPlayer['name']).lower()
    currentPlayerIsBot = (m['players'][currentPlayerIndex]['cpuPPR'] is not None)
    numberOfPlayers = len(m['players'])

    turns = m['turns'][0]
    points = str(turns['points'])


    rounds = m['round']
    throwAmount = len(turns['throws'])
    # type = turns['throws'][throwAmount - 1]['segment']['bed'].lower()
    # field_name = turns['throws'][throwAmount - 1]['segment']['name'].lower()
    # field_multiplier = turns['throws'][throwAmount - 1]['segment']['multiplier']
    # field_number = turns['throws'][throwAmount - 1]['segment']['number']
    pcc_success = False
    isGameFin = False

    # ppi('CurrentPlayerName: ' + currentPlayerName)
    # ppi('CurrentPlayerIsBot: ' + str(currentPlayerIsBot))
    # ppi('rounds: ' + str(rounds))
    # ppi('variant: ' + variant)
    # ppi('target: ' + target)
    # ppi('segment type: ' + type + ' Feld Name: ' + field_name + ' Feld Multiplikator: ' + str(field_multiplier) + ' Feld Nummer: ' + str(field_number))
    # ppi(json.dumps(m, indent = 4, sort_keys = True))
    matchshot = (m['winner'] != -1 and isGameFinished == False)
    gameshot = (m['gameWinner'] != -1 and isGameFinished == False)

    matchon = (turns['throws'] == [] and m['leg'] == 1 and m['set'] == 1 and rounds == 1)
    gameon = (turns['throws'] == [] and rounds == 1)
    
    # BLIND SUPPORT: Announce target at turn start
    if turns['throws'] == []:
        blindSupport.announce_turn_start('Shanghai', m)
    
    # BLIND SUPPORT: Announce dart position
    if turns != None and turns['throws'] != []:
        lastThrow = turns['throws'][-1]
        blindSupport.announce_dart_result('Shanghai', lastThrow)

    # Darts pulled (Playerchange and Possible-checkout)
    if gameon == False and turns != None and turns['throws'] == [] or isGameFinished == True:
        dartsPulled = {
            "event": "darts-pulled",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "game": {
                "mode": variant,
                # TODO: fix
                "dartsThrown": "3",
                "round": str(rounds)
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

            if currentPlayerIsBot == False or CALL_BOT_ACTIONS:

                if pcc_success == False and CALL_CURRENT_PLAYER == 2 and numberOfPlayers > 1:
                    play_sound_effect(currentPlayerName)

            # Player-change
            if pcc_success == False and AMBIENT_SOUNDS != 0.0:
                if play_sound_effect('ambient_playerchange_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                    play_sound_effect('ambient_playerchange', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                

            ppi("Next player")
    
    elif CALL_EVERY_DART > 0 and turns != None and turns['throws'] != [] and len(turns['throws']) >= 1 and matchshot == False and gameshot == False: 
        
        if currentPlayerIsBot == False or CALL_BOT_ACTIONS:
            throwAmount = len(turns['throws'])
            type = turns['throws'][throwAmount - 1]['segment']['bed'].lower()
            field_name = turns['throws'][throwAmount - 1]['segment']['name'].lower()
            field_multiplier = turns['throws'][throwAmount - 1]['segment']['multiplier']
            field_number = turns['throws'][throwAmount - 1]['segment']['number']
            # ppi("Type: " + str(type) + " - Field-name: " + str(field_name))
            # ppi(turns['throws'][throwAmount - 1]['segment'])
                

            # SINGLE-DART-SCORE
            if CALL_EVERY_DART == 1:
                score = field_number * field_multiplier
                play_sound_effect(str(score))

            # SINGLE-DART-NAME
            elif CALL_EVERY_DART == 2:
                if field_number == 25 and field_multiplier == 1:
                    field_name = 'bull'
                elif field_number == 25 and field_multiplier == 2:
                    field_name = 'bullseye'

                # bull
                # bullseye 
                # s1 to t20
                # m1 to m20
                if play_sound_effect(field_name) == False:
                    field_number = str(field_number)

                    if type == 'singleouter' or type == 'singleinner':
                        play_sound_effect(field_number)
                    elif type == 'outside':
                        play_sound_effect(type)
                    else:
                        if play_sound_effect(type):
                            play_sound_effect(field_number, wait_for_last=True)

            # SINGLE-DART-EFFECT
            elif CALL_EVERY_DART == 3:
                if field_number == 25 and field_multiplier == 1:
                    field_name = 'bull'
                elif field_number == 25 and field_multiplier == 2:
                    field_name = 'bullseye'

                # effect_bull
                # effect_bullseye 
                # effect_s1 to effect_t20
                # effect_m1 to effect_m20
                if play_sound_effect('effect_' + field_name, mod = False) == False:

                    # effect_single
                    # effect_singleouter
                    # effect_singleinner
                    inner_outer = False
                    if type == 'singleouter' or type == 'singleinner':
                        inner_outer = play_sound_effect('effect_' + type, mod = False)
                        if inner_outer == False:
                            play_sound_effect('effect_single', mod = False)

                    # effect_double
                    # effect_triple 
                    # effect_outside
                    else:
                        play_sound_effect('effect_' + type, mod = False)
    # Check for matchshot
    if matchshot == True:
        isGameFin = True
        
        matchWon = {
                "event": "match-won",
                "player": currentPlayerName,
                "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
                "game": {
                    "mode": variant,
                    "dartsThrownValue": points
                } 
            }
        broadcast(matchWon)

        if play_sound_effect('matchshot') == False:
            play_sound_effect('gameshot')

        if CALL_CURRENT_PLAYER >= 1:
            play_sound_effect(currentPlayerName, True)

        if AMBIENT_SOUNDS != 0.0:
            if play_sound_effect('ambient_matchshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            elif play_sound_effect('ambient_matchshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            elif play_sound_effect('ambient_gameshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            else:
                play_sound_effect('ambient_gameshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
            

        if RANDOM_CALLER == 2:
            setup_caller()
        ppi('Gameshot and match')

    # Check for gameshot
    elif gameshot == True:
        isGameFin = True
        
        gameWon = {
                "event": "game-won",
                "player": currentPlayerName,
                "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
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
        # maxLeg = m['legs']
        # maxSets = m['sets']

        # ppi('currentLeg: ' + str(currentLeg))
        # ppi('currentSet: ' + str(currentSet))

        isSet = False
        if 'sets' not in m:
            play_sound_effect('leg_' + str(currentLeg), gameshotState)
        else:
            if currentPlayerScoreLegs == 0:
                play_sound_effect('set_' + str(currentSet), gameshotState)
                isSet = True
            else:
                play_sound_effect('leg_' + str(currentLeg), gameshotState)    

        if CALL_CURRENT_PLAYER >= 1:
            play_sound_effect(currentPlayerName, True)

        if AMBIENT_SOUNDS != 0.0:
            if isSet == True:
                if play_sound_effect('ambient_setshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                    pass
                elif play_sound_effect('ambient_setshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                    pass
                elif play_sound_effect('ambient_gameshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                    pass
                else:
                    play_sound_effect('ambient_gameshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    
            else:
                if play_sound_effect('ambient_gameshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                    pass
                else:
                    play_sound_effect('ambient_gameshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

        if RANDOM_CALLER == 2:
            setup_caller()
        ppi('Gameshot')        

    # Check for matchon
    elif matchon == True:
        isGameFinished = False

        currentMatchPlayers = []
        currentMatchHost = None
        if players != []:
            for p in players:
                if 'boardId' in p:
                    if currentMatchHost is None and m['host']['id'] == p['userId'] and p['boardId'] == AUTODART_USER_BOARD_ID:
                        currentMatchHost = True
                    else:
                        currentMatchPlayers.append(p)

        matchStarted = {
            "event": "match-started",
            "id": currentMatch,
            "me": AUTODART_USER_BOARD_ID,
            # "meHost": currentMatchHost,
            # "players": currentMatchPlayers,
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "game": {
                "mode": variant,
                # TODO: fix
                "special": "TODO"
                }     
            }
        broadcast(matchStarted)

        callPlayerNameState = False
        if CALL_CURRENT_PLAYER >= 1:
            callPlayerNameState = play_sound_effect(currentPlayerName)

        if play_sound_effect('matchon', callPlayerNameState, mod = False) == False:
            play_sound_effect('gameon', callPlayerNameState, mod = False)

        if AMBIENT_SOUNDS != 0.0:
            state = play_sound_effect('ambient_matchon_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
            if state == False and play_sound_effect('ambient_matchon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                if play_sound_effect('ambient_gameon_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                    play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)


        ppi('Matchon')

    # Check for gameon
    elif gameon == True:
        isGameFinished = False

        gameStarted = {
            "event": "game-started",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "game": {
                "mode": variant,
                # TODO: fix
                "special": "TODO"
                }     
            }
        broadcast(gameStarted)

        callPlayerNameState = False
        if CALL_CURRENT_PLAYER >= 1:
            callPlayerNameState = play_sound_effect(currentPlayerName)

        play_sound_effect('gameon', callPlayerNameState, mod = False)

        if AMBIENT_SOUNDS != 0.0:
            if play_sound_effect('ambient_gameon_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

        ppi('Gameon')

    # Check for 1. Dart
    elif turns != None and turns['throws'] != [] and len(turns['throws']) == 1:
        isGameFinished = False
        dart1Thrown = {
            "event": "dart1-thrown",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "playerIsBot": str(currentPlayerIsBot),
            "game": {
                "mode": variant,
                "dartNumber": "1",
                "dartValue": points,
                "round": str(rounds)     
            }
        }
        broadcast(dart1Thrown)

    # Check for 2. Dart
    elif turns != None and turns['throws'] != [] and len(turns['throws']) == 2:
        isGameFinished = False
        dart2Thrown = {
            "event": "dart2-thrown",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "playerIsBot": str(currentPlayerIsBot),
            "game": {
                "mode": variant,
                "dartNumber": "2",
                "round": str(rounds)     
            }
        }
        broadcast(dart2Thrown)

    # Check for 3. Dart - Score-call
    elif turns != None and turns['throws'] != [] and len(turns['throws']) == 3:
        isGameFinished = False
        # dart3score = str(int(points) - int(dart1score) - int(dart2score))
        dart3Thrown = {
            "event": "dart3-thrown",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "playerIsBot": str(currentPlayerIsBot),
            "game": {
                "mode": variant,
                "dartNumber": "3",
                "round": str(rounds)      
            }
        }
        broadcast(dart3Thrown)
        dartsThrown = {
            "event": "darts-thrown",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "playerIsBot": str(currentPlayerIsBot),
            "game": {
                "mode": variant,
                "dartNumber": "3",
                "dartValue": points,
                "round": str(rounds)     
            }
        }
        # ppi(dartsThrown)
        broadcast(dartsThrown)

        if currentPlayerIsBot == False or CALL_BOT_ACTIONS:
            if CALL_EVERY_DART == 0 or CALL_EVERY_DART_TOTAL_SCORE == True:
                if int(points) <= 0:
                    points = "0"
                play_sound_effect(points, wait_for_last=CALL_EVERY_DART > 0)

            if AMBIENT_SOUNDS != 0.0:
                ambient_x_success = False

                throw_combo = ''
                for t in turns['throws']:
                    throw_combo += t['segment']['name'].lower()
                # ppi(throw_combo)

                if turns['points'] != 0:
                    ambient_x_success = play_sound_effect('ambient_' + str(throw_combo), AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    if ambient_x_success == False:
                        ambient_x_success = play_sound_effect('ambient_' + str(turns['points']), AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

                if ambient_x_success == False:
                    if turns['points'] >= 150:
                        play_sound_effect('ambient_150more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)   
                    elif turns['points'] >= 120:
                        play_sound_effect('ambient_120more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    elif turns['points'] >= 100:
                        play_sound_effect('ambient_100more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    elif turns['points'] >= 50:
                        play_sound_effect('ambient_50more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    elif turns['points'] >= 1:
                        play_sound_effect('ambient_1more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    else:
                        play_sound_effect('ambient_noscore', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

                # Koordinaten der Pfeile
                coords = []
                for t in turns['throws']:
                    if 'coords' in t:
                        coords.append({"x": t['coords']['x'], "y": t['coords']['y']})

                # ppi(str(coords))

                # Suche das Koordinatenpaar, das am weitesten von den beiden Anderen entfernt ist
                if len(coords) == 3:
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
                        play_sound_effect('ambient_group_legendary', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)   
                    elif group_score >= 95:
                        play_sound_effect('ambient_group_perfect', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    elif group_score >= 92:
                        play_sound_effect('ambient_group_very_nice', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    elif group_score >= 89:
                        play_sound_effect('ambient_group_good', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                    elif group_score >= 86:
                        play_sound_effect('ambient_group_normal', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
     
        ppi("Turn ended")

    mirror_sounds()

    if isGameFin == True:
        isGameFinished = True

def process_match_gotcha(m):
    global indexNameMacro
    global gotcha_last_player_points
    global isGameFinished
    global lastPoints
    global blindSupport
    currentPlayerIndex = m['player']
    currentPlayer = m['players'][currentPlayerIndex]
    currentPlayerName = str(currentPlayer['name']).lower()
    currentPlayerIsBot = (m['players'][currentPlayerIndex]['cpuPPR'] is not None)
    playerCount = len(m['players'])
    turns = m['turns'][0]
    gameScores = m['gameScores']
    points = turns['score']
    variant = m['variant']
    isGameOn = False
    isGameFin = False
    if gotcha_last_player_points == []:
        gotcha_last_player_points = gameScores
    
#    check gamescores
    i = 0
    gameScoreZero = False
    while i <= (playerCount - 1):
        if gameScores[i] == 0:
            gameScoreZero = True
        else:
            gameScoreZero = False
            break
        i += 1
    # ppi("gameScore from other player: "+ str(gotcha_last_player_points[gameScorePlayer]) + " Thrown points: " + str(points))
    # Check if opponend score was reset
    if gameScoreZero == False and points != 0:
        p = 0
        while p <= (playerCount-1):
            if p != currentPlayerIndex:
                if gotcha_last_player_points[p] == points:
                    play_sound_effect("got_score_denied", wait_for_last = True)
            p += 1
    if gotcha_last_player_points != gameScores:
        gotcha_last_player_points = gameScores

    # Call every thrown dart
    if CALL_EVERY_DART > 0 and turns != None and turns['throws'] != [] and len(turns['throws']) >= 1: 

        # BLIND SUPPORT: Announce dart position
        if CALL_BLIND_SUPPORT == 1:
            lastThrow = turns['throws'][-1]
            blindSupport.announce_dart_result('Gotcha', lastThrow)

        elif currentPlayerIsBot == False or CALL_BOT_ACTIONS:

            throwAmount = len(turns['throws'])
            type = turns['throws'][throwAmount - 1]['segment']['bed'].lower()
            field_name = turns['throws'][throwAmount - 1]['segment']['name'].lower()
            field_number = turns['throws'][throwAmount - 1]['segment']['number']
            field_multiplier = turns['throws'][throwAmount - 1]['segment']['multiplier']         

            # SINGLE-DART-SCORE
            if CALL_EVERY_DART == 1:
                score = field_number * field_multiplier
                play_sound_effect(str(score), wait_for_last = True)

            # SINGLE-DART-NAME
            elif CALL_EVERY_DART == 2:
                if field_number == 25 and field_multiplier == 1:
                    field_name = 'bull'
                elif field_number == 25 and field_multiplier == 2:
                    field_name = 'bullseye'

                # bull
                # bullseye 
                # s1 to t20
                # m1 to m20
                if play_sound_effect(field_name) == False:
                    field_number = str(field_number)

                    if type == 'singleouter' or type == 'singleinner':
                        play_sound_effect(field_number, wait_for_last=True)
                    elif type == 'outside':
                        play_sound_effect(type)
                    else:
                        if play_sound_effect(type, wait_for_last=True):
                            play_sound_effect(field_number, wait_for_last=True)

            # SINGLE-DART-EFFECT
            elif CALL_EVERY_DART == 3:
                if field_number == 25 and field_multiplier == 1:
                    field_name = 'bull'
                elif field_number == 25 and field_multiplier == 2:
                    field_name = 'bullseye'

                # effect_bull
                # effect_bullseye 
                # effect_s1 to effect_t20
                # effect_m1 to effect_m20
                if play_sound_effect('effect_' + field_name, mod = False) == False:

                    # effect_single
                    # effect_singleouter
                    # effect_singleinner
                    inner_outer = False
                    if type == 'singleouter' or type == 'singleinner':
                        inner_outer = play_sound_effect('effect_' + type, mod = False)
                        if inner_outer == False:
                            play_sound_effect('effect_single', mod = False)

                    # effect_double
                    # effect_triple 
                    # effect_outside
                    else:
                        play_sound_effect('effect_' + type, mod = False)
    # Check for matchshot
    if m['winner'] != -1 and isGameFinished == False:
        isGameFin = True

        throwPoints = 0
        lastPoints = ''
        for t in turns['throws']:
            number = t['segment']['number']
            throwPoints += (t['segment']['multiplier'] * number)
            lastPoints += 'x' + str(t['segment']['name'])
        lastPoints = lastPoints[1:]
        
        matchWon = {
                "event": "match-won",
                "player": currentPlayerName,
                "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
                "game": {
                    "mode": variant,
                    "dartsThrownValue": throwPoints                    
                } 
            }
        broadcast(matchWon)

        if play_sound_effect('matchshot', wait_for_last=True) == False:
            play_sound_effect('gameshot', wait_for_last=True)
        play_sound_effect(currentPlayerName, True)
        
        if AMBIENT_SOUNDS != 0.0:
            if play_sound_effect('ambient_matchshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            elif play_sound_effect('ambient_matchshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            elif play_sound_effect('ambient_gameshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            else:
                play_sound_effect('ambient_gameshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
        
        setup_caller()
        ppi('Gameshot and match')

    # Check for gameshot
    elif m['gameWinner'] != -1 and isGameFinished == False:
        isGameFin = True

        throwPoints = 0
        lastPoints = ''
        for t in turns['throws']:
            number = t['segment']['number']
            throwPoints += (t['segment']['multiplier'] * number)
            lastPoints += 'x' + str(t['segment']['name'])
        lastPoints = lastPoints[1:]
        
        gameWon = {
                "event": "game-won",
                "player": currentPlayerName,
                "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
                "game": {
                    "mode": variant,
                    "dartsThrownValue": throwPoints
                } 
            }
        broadcast(gameWon)

        play_sound_effect('gameshot')
        play_sound_effect(currentPlayerName, True)
        
        if AMBIENT_SOUNDS != 0.0:
            if play_sound_effect('ambient_gameshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            else:
                play_sound_effect('ambient_gameshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
        
        if RANDOM_CALLER == 2:
            setup_caller()
        ppi('Gameshot')
    
    # Check for matchon
    elif m['gameScores'][0] == 0 and m['scores'] == None and turns['throws'] == [] and m['round'] == 1 and m['leg'] == 1 and m['set'] == 1:
        isGameOn = True
        isGameFinished = False

        matchStarted = {
            "event": "match-started",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
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
        # if AMBIENT_SOUNDS != 0.0 and ('legs' in m and 'sets'):
        #     if play_sound_effect('ambient_matchon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS) == False:
        #         play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS)
        if AMBIENT_SOUNDS != 0.0:
            state = play_sound_effect('ambient_matchon_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
            if state == False and play_sound_effect('ambient_matchon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                if play_sound_effect('ambient_gameon_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                    play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)    
        
        ppi('Matchon')

    # Check for gameon
    elif m['gameScores'][0] == 0 and m['scores'] == None and turns['throws'] == [] and m['round'] == 1:
        isGameOn = True
        isGameFinished = False
        
        gameStarted = {
            "event": "game-started",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
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
            if play_sound_effect('ambient_gameon_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

        ppi('Gameon')

        if currentPlayerIsBot == False or CALL_BOT_ACTIONS:
            play_sound_effect('busted')
            if AMBIENT_SOUNDS != 0.0:
                play_sound_effect('ambient_noscore', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
            ppi('Busted')

    # Check for 1. Dart
    elif turns != None and turns['throws'] != [] and len(turns['throws']) == 1:
        isGameFinished = False

    # Check for 2. Dart
    elif turns != None and turns['throws'] != [] and len(turns['throws']) == 2:
        isGameFinished = False

    # Check for 3. Dart - points call
    elif turns != None and turns['throws'] != [] and len(turns['throws']) == 3:
        isGameFinished = False

        # TODO fields already closed?
        throwPoints = 0
        lastPoints = ''
        for t in turns['throws']:
            number = t['segment']['number']
            throwPoints += (t['segment']['multiplier'] * number)
            lastPoints += 'x' + str(t['segment']['name'])
        lastPoints = lastPoints[1:]

        dartsThrown = {
            "event": "darts-thrown",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "playerIsBot": str(currentPlayerIsBot),
            "game": {
                "mode": variant,
                "dartNumber": "3",
                "dartValue": throwPoints,        

            }
        }
        broadcast(dartsThrown)

        if currentPlayerIsBot == False or CALL_BOT_ACTIONS:
            if CALL_EVERY_DART == 0 or CALL_EVERY_DART_TOTAL_SCORE == True:
                play_sound_effect(str(throwPoints), wait_for_last=CALL_EVERY_DART != 0)

            if AMBIENT_SOUNDS != 0.0:
                if throwPoints == 0:
                    play_sound_effect('ambient_noscore', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                elif throwPoints == 180:
                    play_sound_effect('ambient_180', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                elif throwPoints >= 153:
                    play_sound_effect('ambient_150more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)   
                elif throwPoints >= 120:
                    play_sound_effect('ambient_120more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                elif throwPoints >= 100:
                    play_sound_effect('ambient_100more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                elif throwPoints >= 50:
                    play_sound_effect('ambient_50more', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

        ppi("Turn ended")
    

    # Playerchange
    if isGameOn == False and turns != None and turns['throws'] == [] or isGameFinished == True:
        dartsPulled = {
            "event": "darts-pulled",
            "player": currentPlayerName,
            "playerIndex": str(indexNameMacro[currentPlayerName.lower()]),
            "game": {
                "mode": variant,
                # TODO: fix
                "dartsThrown": "3",
                "dartsThrownValue": lastPoints,
                # TODO: fix
                # "darts": [
                #     {"number": "1", "value": "60"},
                #     {"number": "2", "value": "60"},
                #     {"number": "3", "value": "60"}
                # ]
            }
        }
        broadcast(dartsPulled)

        if currentPlayerIsBot == False or CALL_BOT_ACTIONS:
            if CALL_CURRENT_PLAYER == 2:
                play_sound_effect(currentPlayerName)

        if AMBIENT_SOUNDS != 0.0:
            if play_sound_effect('ambient_playerchange_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                play_sound_effect('ambient_playerchange', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
        
        ppi("Next player")

    mirror_sounds()

    if isGameFin == True:
        isGameFinished = True

def process_common(m):
    broadcast(m)

def mute_audio_background(vol):
    global background_audios
    session_fails = 0
    for session in background_audios:
        try:
            volume = session.SimpleAudioVolume
            if session.Process and session.Process.name() != "darts-caller.exe":
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
                if session.Process and session.Process.name() != "darts-caller.exe":
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



def connect_autodarts():
    global BOARD_OWNER
    global USER_LOCATION
    global USER_ID
    global USER_NAME

    res2 = requests.get(AUTODARTS_BOARDS_URL + AUTODART_USER_BOARD_ID, headers = {'Authorization': f'Bearer {kc.access_token}'})
    # ppi(json.dumps(res2.json(), indent = 4, sort_keys = True))
    if 'country' in res2.json()['permissions'][0]['user']:
        userlocationtemp = res2.json()['permissions'][0]['user']['country']
        USER_LOCATION = str(userlocationtemp)
    else:
        USER_LOCATION = "undefined"
    if 'name' in res2.json()['permissions'][0]['user']:
        usernametemp = res2.json()['permissions'][0]['user']['name']
        USER_NAME = str(usernametemp)
    else:
        USER_NAME = None
    if 'id' in res2.json()['permissions'][0]['user']:
        useridtemp = res2.json()['permissions'][0]['user']['id']
        USER_ID = str(useridtemp)
    else:
        USER_ID = None
    # res2 = res2.json()['']
    # ppi(json.dumps(res2, indent = 4, sort_keys = True))
    # res2 = res2['permissions']
    #ppi(res2)
    BOARD_OWNER = str(usernametemp)
   # ppi('Board owner: ' + BOARD_OWNER)  
    send_arguments_to_php(DB_INSERT, DB_ARGS,CALLER_SETTINGS_ARGS)

    def process(*args):
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(AUTODARTS_WEBSOCKET_URL,
                                    header={'Authorization': f'Bearer {kc.access_token}'},
                                    on_open = on_open_autodarts,
                                    on_message = on_message_autodarts,
                                    on_error = on_error_autodarts,
                                    on_close = on_close_autodarts)
        sslOptions = {"cert_reqs": ssl.CERT_NONE}
        if CERT_CHECK:
            sslOptions = None
        ws.run_forever(sslopt=sslOptions)
    threading.Thread(target=process).start()

    

def on_open_autodarts(ws):
    global BOARD_OWNER
    # fetch-matches
    # get
    # https://api.autodarts.io/gs/v0/matches/
    try:
        res = requests.get(AUTODARTS_MATCHES_URL, headers = {'Authorization': f'Bearer {kc.access_token}'})
        res = res.json()
        # ppi(json.dumps(res, indent = 4, sort_keys = True))

        # watchout for a match with my board-id
        should_break = False
        for m in res:
            for p in m['players']:
                if 'boardId' in p and p['boardId'] == AUTODART_USER_BOARD_ID:
                    mes = {
                        "event": "start",
                        "id": m['id']
                    }
                    listen_to_match(mes, ws)
                    should_break = True
                    break
            if should_break:
                break
            
    except Exception as e:
        ppe('Fetching matches failed', e)

    
    try:
        paramsSubscribeMatchesEvents = {
            "channel": "autodarts.boards",
            "type": "subscribe",
            "topic": AUTODART_USER_BOARD_ID + ".matches"
        }
        ws.send(json.dumps(paramsSubscribeMatchesEvents))

        ppi('Receiving live information for board-id: ' + AUTODART_USER_BOARD_ID)

    except Exception as e:
        ppe('WS-Open-boards failed: ', e)


    try:
        paramsSubscribeUserEvents = {
            "channel": "autodarts.users",
            "type": "subscribe",
            "topic": kc.user_id + ".events"
        }
        ws.send(json.dumps(paramsSubscribeUserEvents))

        # ppi('Receiving live information for user-id: ' + kc.user_id)

    except Exception as e:
        ppe('WS-Open-users failed: ', e)
    
   

def on_message_autodarts(ws, message):
    def process(*args):
        try:
            global currentMatch
            global lobbyPlayers
            global lastMessage
            global gotcha_last_player_points
            global indexNameMacro
            global matchIsActive
            global match_lock
            m = json.loads(message)
            
            # ppi(json.dumps(m, indent = 4, sort_keys = True))
            if m['channel'] == 'autodarts.matches':
                data = m['data']
                # ppi(json.dumps(data, indent = 4, sort_keys = True))
                if indexNameMacro == {}:
                    map_playerIndex_to_name(data, False)

                # ppi(json.dumps(data, indent = 4, sort_keys = True))
                # if m['topic'].endswith('game-events'):
                #     ppi(json.dumps(data, indent = 4, sort_keys = True))

                # ppi('Current Match: ' + currentMatch)
                
                if('turns' in data and len(data['turns']) >=1):
                    data['turns'][0].pop("id", None)
                    data['turns'][0].pop("createdAt", None)
                
                time.sleep(0.01)

                # Thread-safe Match-Validierung
                with match_lock:
                    if not matchIsActive:
                        return
                    
                    if currentMatch is None:
                        return
                    
                    if 'id' not in data or data['id'] != currentMatch:
                        return
                    
                    # Doppelte Event-Prüfung
                    if lastMessage == data:
                        return
                        
                    lastMessage = data
                
                # Rest der Verarbeitung außerhalb des Locks
                # ppi(json.dumps(data, indent = 4, sort_keys = True))

                # process_common(data)

                variant = data['variant']
                
                if variant == 'Bull-off':
                    process_bulling(data)

                elif variant == 'X01' or variant == 'Random Checkout':
                    process_match_x01(data)
                    
                elif variant == 'Cricket':
                    process_match_cricket(data)
                
                elif variant == 'ATC':
                    process_match_atc(data)

                elif variant == 'RTW':
                    process_match_rtw(data)
               
                elif variant == 'CountUp':
                    process_match_CountUp(data)

                elif variant == 'Bermuda':
                    process_match_Bermuda(data)
                
                elif variant == 'Shanghai':
                    process_match_shanghai(data)

                elif variant == 'Gotcha':
                    process_match_gotcha(data)

            elif m['channel'] == 'autodarts.boards':
                data = m['data']
                # ppi(json.dumps(data, indent = 4, sort_keys = True))
                # GET BOARD STATUS
                if data['event'] == 'Manual reset' or data['event'] == 'Started' or data['event'] == 'Stopped' or data['event'] == 'Takeout started' or data['event'] == 'Takeout finished' or data['event'] == 'Calibration started' or data['event'] == 'Calibration finished':
                    board_status_message(m)
                    # ppi('New Params')
                listen_to_match(data, ws)
            
            elif m['channel'] == 'autodarts.users':
                data = m['data']
                # ppi(json.dumps(data, indent = 4, sort_keys = True))
                if 'event' in data:
                    if data['event'] == 'lobby-enter':
                        # ppi("lobby-enter", data)

                        lobby_id = data['body']['id']
                        currentMatch = 'lobby:' + lobby_id

                        ppi('Listen to lobby: ' + lobby_id)
                        paramsSubscribeLobbyEvents = {
                                "channel": "autodarts.lobbies",
                                "type": "subscribe",
                                "topic": lobby_id + ".state"
                            }
                        ws.send(json.dumps(paramsSubscribeLobbyEvents))
                        paramsSubscribeLobbyEvents = {
                                "channel": "autodarts.lobbies",
                                "type": "subscribe",
                                "topic": lobby_id + ".events"
                            }
                        ws.send(json.dumps(paramsSubscribeLobbyEvents))
                        lobbyPlayers = []

                        if play_sound_effect("ambient_lobby_in", False, mod = False):
                            mirror_sounds()

                    elif data['event'] == 'lobby-leave':
                        # ppi("lobby-leave", data)

                        lobby_id = data['body']['id']
                        currentMatch = None

                        ppi('Stop Listen to lobby: ' + lobby_id)
                        ppi('I left the lobby, message from autodarts.users')
                        paramsUnsubscribeLobbyEvents = {
                                "channel": "autodarts.lobbies",
                                "type": "unsubscribe",
                                "topic": lobby_id + ".state"
                            }
                        ws.send(json.dumps(paramsUnsubscribeLobbyEvents))
                        paramsUnsubscribeLobbyEvents = {
                                "channel": "autodarts.lobbies",
                                "type": "unsubscribe",
                                "topic": lobby_id + ".events"
                            }
                        ws.send(json.dumps(paramsUnsubscribeLobbyEvents))
                        lobbyPlayers = []

                        if play_sound_effect("ambient_lobby_out", False, mod = False):
                            mirror_sounds()

            elif m['channel'] == 'autodarts.lobbies':
                data = m['data']
                # ppi(json.dumps(data, indent = 4, sort_keys = True))
                
                if 'event' in data:
                    if data['event'] == 'start':
                        # ppi(json.dumps(data, indent = 4, sort_keys = True))
                        map_playerIndex_to_name(data, True)
                        pass

                    elif data['event'] == 'finish' or data['event'] == 'delete':
                        ppi('Stop listening to lobby: ' + m['id'])
                        ppi('Lobby finished or deleted, message from autodarts.lobbies')
                        paramsUnsubscribeLobbyEvents = {
                            "type": "unsubscribe",
                            "channel": "autodarts.lobbies",
                            "topic": m['id'] + ".events"
                        }
                        ws.send(json.dumps(paramsUnsubscribeLobbyEvents))
                        paramsUnsubscribeLobbyEvents = {
                            "type": "unsubscribe",
                            "channel": "autodarts.lobbies",
                            "topic": m['id'] + ".state"
                        }
                        ws.send(json.dumps(paramsUnsubscribeLobbyEvents))
                        lobbyPlayers = []
                        ppi ("Player index reset")
                        gotcha_last_player_points=[]
                        indexNameMacro = {}
                        # currentMatch = None
                        if play_sound_effect("ambient_lobby_out", False, mod = False):
                            mirror_sounds()
  

                elif 'players' in data:
                    # did I left the lobby?
                    me = False
                    for p in data['players']:
                        if 'boardId' in p and p['boardId'] == AUTODART_USER_BOARD_ID:
                            me = True
                            break
                    if me == False:
                        lobby_id = data['id']

                        ppi('Stop Listen to lobby: ' + lobby_id)
                        ppi('I left the lobby, message from autodarts.lobbies')
                        paramsUnsubscribeLobbyEvents = {
                                "channel": "autodarts.lobbies",
                                "type": "unsubscribe",
                                "topic": lobby_id + ".state"
                            }
                        ws.send(json.dumps(paramsUnsubscribeLobbyEvents))
                        paramsUnsubscribeLobbyEvents = {
                                "channel": "autodarts.lobbies",
                                "type": "unsubscribe",
                                "topic": lobby_id + ".events"
                            }
                        ws.send(json.dumps(paramsUnsubscribeLobbyEvents))
                        if play_sound_effect("ambient_lobby_out", False, mod = False):
                            mirror_sounds()
                        lobbyPlayers = []
                        currentMatch = None
                        return
                        

                    # check for left players
                    lobbyPlayersLeft = []
                    for lp in lobbyPlayers:
                        player_found = False
                        for p in data['players']:
                            if p['userId'] == lp['userId']:
                                player_found = True
                                break
                        if player_found == False:
                            lobbyPlayersLeft.append(lp)

                    for lpl in lobbyPlayersLeft:
                        lobbyPlayers.remove(lpl)
                        player_name = str(lpl['name']).lower()
                        ppi(player_name + " left the lobby")

                        play_sound_effect('ambient_lobby_out', False, mod = False)

                        if check_sounds([player_name, 'left']):
                            play_sound_effect(player_name, True)
                            play_sound_effect('left', True)
                        
                        playerLeft = {
                            "event": "lobby",
                            "action": "player-left",
                            "player": player_name
                        }
                        broadcast(playerLeft)


                    # check for joined players
                    for p in data['players']:
                        player_id = p['userId']
                        if 'boardId' in p and p['boardId'] != AUTODART_USER_BOARD_ID and not any(lobbyPlayer['userId'] == player_id for lobbyPlayer in lobbyPlayers):
                            lobbyPlayers.append(p)
                            player_name = str(p['name']).lower()
                            player_avg = get_player_average(player_id)
                            if player_avg != None:
                                player_avg = str(math.ceil(player_avg))

                            ppi(player_name + " (" + player_avg + " average) joined the lobby")

                            play_sound_effect('ambient_lobby_in', False, mod = False)

                            if check_sounds([player_name, 'average', player_avg]):
                                play_sound_effect(player_name, True)
                                if player_avg != None:
                                    play_sound_effect('average', True)
                                    play_sound_effect(player_avg, True)
                            
                            playerJoined = {
                                "event": "lobby",
                                "action": "player-joined",
                                "player": player_name,
                                "average": player_avg
                            }
                            broadcast(playerJoined)
                            break
                    mirror_sounds()
            
            else:
                ppi('INFO: unexpected ws-message')
                # ppi(json.dumps(m, indent = 4, sort_keys = True))
                

        except Exception as e:
            ppe('WS-Message failed: ', e)

    threading.Thread(target=process).start()

def map_playerIndex_to_name(msg,lobby):
    global indexNameMacro
    if lobby == True:
        if msg != None and 'body' in msg:
            playerAmount = len(msg['body']['players'])
            if playerAmount > 0:
                for i in range(0, playerAmount):
                    playerName = msg['body']['players'][i]['name']
                    # playerIndex = msg['players'][i]['index']
                    if playerName != None:
                        playerName = str(playerName).lower()
                        indexNameMacro[playerName] = i
                    else:
                        indexNameMacro[i] = None
    else:
        if msg != None and 'players' in msg:
            playerAmount = len(msg['players'])
            if playerAmount > 0:
                for i in range(0, playerAmount):
                    playerName = msg['players'][i]['name']
                    # playerIndex = msg['players'][i]['index']
                    if playerName != None:
                        playerName = str(playerName).lower()
                        indexNameMacro[playerName] = i
                    else:
                        indexNameMacro[i] = None

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

 
def start_webserver(host, port, ssl_context=None):
    if ssl_context is None:
        socketio.run(app, host=host, port=port, debug=False, allow_unsafe_werkzeug=True)
    else:
        socketio.run(app, host=host, port=port, debug=False, allow_unsafe_werkzeug=True, ssl_context=ssl_context)

def broadcast(data):
    socketio.emit('message', data)

def unicast(client, data):
    socketio.emit('message', data, room=client)


@socketio.on('connect')
def handle_connect():
    global webCallerSyncs
    cid = str(request.sid)
    ppi('NEW CLIENT CONNECTED: ' + cid)
    if cid not in webCallerSyncs or webCallerSyncs[cid] is None:
        webCallerSyncs[cid] = queue.Queue()
    ppi (webCallerSyncs)
    
    

@socketio.on('disconnect')
def handle_disconnect():
    cid = str(request.sid)
    ppi('CLIENT DISCONNECTED: ' + cid)
    if cid in webCallerSyncs:
        webCallerSyncs[cid] = None
            
@socketio.on('message')
def handle_message(message):
    ppi(message)
    try:
        global CALLER
        global RANDOM_CALLER
        global RANDOM_CALLER_LANGUAGE
        global RANDOM_CALLER_GENDER
        global CALL_EVERY_DART
        global CALL_CURRENT_PLAYER
        global CALL_BOT_ACTIONS
        global POSSIBLE_CHECKOUT_CALL
        global POSSIBLE_CHECKOUT_CALL_YOURSELF_ONLY
        global isBullingFinished
        global isGameFinished
        global caller_profiles_favoured
        global EXT_WLED
        global EXT_PIXEL

        cid = str(request.sid)

        if type(message) == str:
       
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
                        
                        start_board()
                        
                    elif message == 'board-stop':
                        stop_board()

                    elif message == 'board-reset':
                        reset_board()

                    elif message == 'board-calibrate':
                        calibrate_board()

                    else:
                        ppi('message', 'This message is not supported')  

                else:
                    ppi('message', 'Can not change board-state as board-address is unknown!')  

            elif message.startswith('correct'):
                msg_splitted = message.split(':')
                throw_indices = msg_splitted[1:-1]
                score = msg_splitted[-1]
                correct_throw(throw_indices, score)
                    
            elif message.startswith('next'):
                if currentMatch is not None:

                    if currentMatch.startswith('lobby'):
                        start_match(currentMatch.split(':')[1])
                    elif isBullingFinished == True:
                        isBullingFinished = False
                        next_game()
                    elif isGameFinished == False:
                        next_throw()
                    else:
                        next_game()

            elif message.startswith('undo'):
                undo_throw()

            elif message.startswith('ban'):
                CALLER = DEFAULT_CALLER
                if len(message.split(':')) > 1:
                    RANDOM_CALLER = 1
                    ban_caller(only_change=True)
                else:
                    ban_caller(False)

            elif message.startswith('caller'):
                messsageSplitted = message.split(':')
                if len(messsageSplitted) > 1:
                    RANDOM_CALLER = 0
                    CALLER = messsageSplitted[1]
                    setup_caller(hi=True)

            elif message.startswith('language'):
                messsageSplitted = message.split(':')
                if len(messsageSplitted) > 1:
                    CALLER = DEFAULT_CALLER
                    RANDOM_CALLER = 1
                    RANDOM_CALLER_LANGUAGE = int(messsageSplitted[1])
                    setup_caller(hi = True)

            elif message.startswith('gender'):
                messsageSplitted = message.split(':')
                if len(messsageSplitted) > 1:
                    CALLER = DEFAULT_CALLER
                    RANDOM_CALLER = 1
                    RANDOM_CALLER_GENDER = int(messsageSplitted[1])                   
                    setup_caller(hi = True)

            elif message.startswith('fav'):
                messsageSplitted = message.split(':')
                if len(messsageSplitted) > 1:
                    if messsageSplitted[1] == '0':
                        favor_caller(unfavor = True)
                    else:
                        favor_caller(unfavor = False)

            elif message.startswith('arg'):
                messsageSplitted = message.split(':')
                if len(messsageSplitted) == 3:
                    arg_name = messsageSplitted[1]
                    arg_value = messsageSplitted[2]
                    if arg_name == 'e':
                        CALL_EVERY_DART = int(arg_value)
                    elif arg_name == 'ccp':
                        CALL_CURRENT_PLAYER = int(arg_value)
                    elif arg_name == 'cba':
                        CALL_BOT_ACTIONS = arg_value == "1"
                    elif arg_name == 'pcc':
                        POSSIBLE_CHECKOUT_CALL = int(arg_value)
                    elif arg_name == 'pccyo':
                        POSSIBLE_CHECKOUT_CALL_YOURSELF_ONLY = arg_value == "1"

            elif message.startswith('call'):
                to_call = message.split(':')[1]
                call_parts = to_call.split(' ')
                for cp in call_parts:
                    play_sound_effect(cp, wait_for_last=False, volume_mult=1.0)
                mirror_sounds()

            elif message.startswith('hello'):
                welcome_event = {
                    "event": "welcome",
                    "callersAvailable": callers_available,
                    "callersFavoured": caller_profiles_favoured,
                    "caller": caller_title_without_version
                }
                unicast(cid, welcome_event)

        elif type(message) == dict:
            
            if 'event' in message:
                event = message['event']

                if event == 'sync' and caller is not None:                    
                    if 'parted' in message:
                        webCallerSyncs[cid].put(message['exists'])

                        partsNeeded = message['parted']
                        
                        existing = []
                        if webCallerSyncs[cid].qsize() == partsNeeded:
                            while partsNeeded > 0:
                                partsNeeded -= 1
                                existing += webCallerSyncs[cid].get()
                            webCallerSyncs[cid].task_done()
                        else:
                            return
                        
                        new = []
                        for key, value in caller.items():
                            for sound_file in value:
                                base_name = os.path.basename(sound_file)
                                if base_name not in existing:
                                    with open(sound_file, 'rb') as file:
                                        encoded_file = (base64.b64encode(file.read())).decode('ascii')
                                    new.append({"name": base_name, "path": quote(sound_file, safe=""), "file": encoded_file})

                        unicast(cid, {"exists": new})

                    else:
                        new = [{"name": os.path.basename(sound_file), "path": quote(sound_file, safe=""), "file": (base64.b64encode(open(sound_file, 'rb').read())).decode('ascii')} for key, value in caller.items() for sound_file in value if os.path.basename(sound_file) not in message['exists']]
                        message['exists'] = new
                        unicast(cid, message)
            
            

    except Exception as e:
        ppe('WS-Client-Message failed.', e)
    if type(message) == dict:
        if 'status' in message:
            if message['status'] == 'WLED connected':
                ppi('WLED connected')
                EXT_WLED = True
                DB_ARGS['wled_version'] = message['version']

                if 'settings' in message:
                    try:
                        wledsettings_json = json.dumps(message['settings'])
                        # ppi(f"Processed WLED settings:\n{wledsettings_json}")
                        DB_ARGS['wled_settings'] = wledsettings_json  # WLED-Settings hinzufügen
                        # ppi(f"DB_ARGS: {DB_ARGS}")
                    except Exception as e:
                        ppe("Failed to process WLED settings.", e)
                send_arguments_to_php(DB_INSERT, DB_ARGS, CALLER_SETTINGS_ARGS)
            elif message['status'] == 'Pixel connected':
                ppi('Pixel connected')
                EXT_PIXEL = True
                DB_ARGS['pixel_version'] = message['version']
                if 'settings' in message:
                    try:
                        pixelsettings_json = json.dumps(message['settings'])
                        # ppi(f"Processed WLED settings:\n{wledsettings_json}")
                        DB_ARGS['pixel_settings'] = pixelsettings_json  # WLED-Settings hinzufügen
                        # ppi(f"DB_ARGS: {DB_ARGS}")
                    except Exception as e:
                        ppe("Failed to process WLED settings.", e)
                send_arguments_to_php(DB_INSERT, DB_ARGS, CALLER_SETTINGS_ARGS)

@app.route('/')
def index():
    return render_template('index.html',    app_version=VERSION, 
                                            db_name=WEB_DB_NAME, 
                                            id=currentMatch,
                                            me=AUTODART_USER_BOARD_ID,
                                            meHost=currentMatchHost,
                                            players=currentMatchPlayers,
                                            languages=CALLER_LANGUAGES, 
                                            genders=CALLER_GENDERS,
                                            language=RANDOM_CALLER_LANGUAGE,
                                            gender=RANDOM_CALLER_GENDER,
                                            every_dart=CALL_EVERY_DART,
                                            call_current_player=CALL_CURRENT_PLAYER,
                                            call_bot_actions=CALL_BOT_ACTIONS,
                                            checkout_call=POSSIBLE_CHECKOUT_CALL,
                                            checkout_call_yourself=POSSIBLE_CHECKOUT_CALL_YOURSELF_ONLY
                                            )
    
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

def send_arguments_to_php(url, args_version, args_caller):
    global EXT_WLED
    global EXT_PIXEL
    global BOARD_OWNER
    global USER_ID
    global USER_NAME
    global USER_LOCATION
    args_version['darts_wled'] = EXT_WLED
    args_version['darts_pixel'] = EXT_PIXEL
    args_version['userID'] = USER_NAME
    args_version['location'] = USER_LOCATION
    # ppi(json.dumps(args_caller, indent=4, sort_keys=True))

    # ppi(f"Sending args_version: {args_version}")
    # ppi(f"Sending args_caller: {args_caller}")
    # args_caller = json.dumps(args_caller)
    
    # URL-Validierung
    if not url.startswith("http"):
        ppi(f"Invalid URL: {url}")
        return
    
    if not args_version or not args_caller:
        ppi("Error: args_version or args_caller is empty!")
        return
    if USER_NAME is not None:
        try:
            # Debugging: Ausgabe der Anfrage-Details
            # ppi(f"Debugging POST Request:")
            # ppi(f"URL: {url}")
            # ppi(f"Data: {json.dumps({**args_version, **args_caller})}")
    
            # POST-Anfrage mit JSON und Formulardaten senden
            response = requests.post(
                url,
                data={**args_version, **args_caller},  # Kombiniere beide Dictionaries
                verify=False
            )
            if response.status_code == 200:
                if DEBUG == 1:
                    ppi("User stats sent successfully")
                    ppi(f"Response: {response.text}")  # Antwortinhalt ausgeben
            else:
                if DEBUG == 1:
                    ppi(f"Failed to send arguments. Status code: {response.status_code}")
                    ppi(f"Response: {response.text}")  # Antwortinhalt ausgeben
        except Exception as e:
            if DEBUG == 1:
                ppi(f"An error occurred: {e}")
    else:
        if DEBUG == 1:
            ppi("User stats not sent, as user-name is unknown")
    # ppi(args)
    # if USER_NAME != None:
    #     try:
    #         response = requests.post(url, data=args_version,json=args_caller,verify=False)
    #         if response.status_code == 200:
    #             ppi("User stats sent successfully")
    #         else:
    #             ppi(f"Failed to send arguments. Status code: {response.status_code}")
    #     except Exception as e:
    #         ppi(f"An error occurred: {e}")
    # else:
    #     ppi("User stats not sent, as user-name is unknown")






if __name__ == "__main__":
    check_already_running()
        
    ap = CustomArgumentParser()
    
    ap.add_argument("-U", "--autodarts_email", required=True, help="Registered email address at " + AUTODARTS_URL)
    ap.add_argument("-P", "--autodarts_password", required=True, help="Registered password address at " + AUTODARTS_URL)
    ap.add_argument("-B", "--autodarts_board_id", required=True, help="Registered board-id at " + AUTODARTS_URL)
    ap.add_argument("-M", "--media_path", required=True, help="Absolute path to your media")
    ap.add_argument("-MS", "--media_path_shared", required=False, default=DEFAULT_EMPTY_PATH, help="Absolute path to shared media folder (every caller get sounds)")
    ap.add_argument("-V", "--caller_volume", type=float, default=DEFAULT_CALLER_VOLUME, required=False, help="Sets calling-volume between 0.0 (silent) and 1.0 (max)")
    ap.add_argument("-C", "--caller", default=DEFAULT_CALLER, required=False, help="Sets a specific caller (voice-pack) for calling")
    ap.add_argument("-R", "--random_caller", type=int, choices=range(0, 3), default=DEFAULT_RANDOM_CALLER, required=False, help="If '1', the application will randomly choose a caller each game. It only works when your base-media-folder has subfolders with its files")
    ap.add_argument("-RL", "--random_caller_language", type=int, choices=range(0, len(CALLER_LANGUAGES) + 1), default=DEFAULT_RANDOM_CALLER_LANGUAGE, required=False, help="If '0', the application will allow every language.., else it will limit caller selection by specific language")
    ap.add_argument("-RG", "--random_caller_gender", type=int, choices=range(0, len(CALLER_GENDERS) + 1), default=DEFAULT_RANDOM_CALLER_GENDER, required=False, help="If '0', the application will allow every gender.., else it will limit caller selection by specific gender")
    ap.add_argument("-CCP", "--call_current_player", type=int, choices=range(0, 3), default=DEFAULT_CALL_CURRENT_PLAYER, required=False, help="If '1', the application will call who is the current player to throw")
    ap.add_argument("-CBA", "--call_bot_actions", type=int, choices=range(0, 2), default=DEFAULT_CALL_BOT_ACTIONS, required=False, help="If '1', the application will call bot actions")
    ap.add_argument("-E", "--call_every_dart", type=int, choices=range(0, 4), default=DEFAULT_CALL_EVERY_DART, required=False, help="If '1', the application will call every thrown dart")
    ap.add_argument("-ETS", "--call_every_dart_total_score", type=int, choices=range(0, 2), default=DEFAULT_CALL_EVERY_DART_TOTAL_SCORE, required=False, help="If '1', the application will call total-score if call-every-dart is active")
    ap.add_argument("-PCC", "--possible_checkout_call", type=int, default=DEFAULT_POSSIBLE_CHECKOUT_CALL, required=False, help="If '1', the application will call a possible checkout starting at 170")
    ap.add_argument("-PCCYO", "--possible_checkout_call_yourself_only", type=int, choices=range(0, 2), default=DEFAULT_POSSIBLE_CHECKOUT_CALL_YOURSELF_ONLY, required=False, help="If '1' the caller will only call if there is a checkout possibility if the current player is you")
    ap.add_argument("-A", "--ambient_sounds", type=float, default=DEFAULT_AMBIENT_SOUNDS, required=False, help="If > '0.0' (volume), the application will call a ambient_*-Sounds")
    ap.add_argument("-AAC", "--ambient_sounds_after_calls", type=int, choices=range(0, 2), default=DEFAULT_AMBIENT_SOUNDS_AFTER_CALLS, required=False, help="If '1', the ambient sounds will appear after calling is finished") 
    ap.add_argument("-DL", "--downloads", type=int, choices=range(0, 101), default=DEFAULT_DOWNLOADS, required=False, help="If > '1', the application will download specified number of available voice-packs")
    ap.add_argument("-DLLA", "--downloads_language", type=int, choices=range(0, len(CALLER_LANGUAGES) + 1), default=DEFAULT_DOWNLOADS_LANGUAGE, required=False, help="If '0', the application will download speakers of every language.., else it will limit speaker downloads by specific language")
    ap.add_argument("-DLN", "--downloads_name", default=DEFAULT_DOWNLOADS_NAME, required=False, help="Sets a specific caller (voice-pack) for download")
    ap.add_argument("-ROVP", "--remove_old_voice_packs", type=int, choices=range(0, 2), default=DEFAULT_REMOVE_OLD_VOICE_PACKS, required=False, help="Removes old voice-packs")
    ap.add_argument("-BAV","--background_audio_volume", required=False, type=float, default=DEFAULT_BACKGROUND_AUDIO_VOLUME, help="Set background-audio-volume between 0.1 (silent) and 1.0 (no mute)")
    ap.add_argument("-LPB", "--local_playback", type=int, choices=range(0, 2), default=DEFAULT_LOCAL_PLAYBACK, required=False, help="If '1' the application will playback audio on your local device.")
    ap.add_argument("-WEBDH", "--web_caller_disable_https", required=False, type=int, choices=range(0, 2), default=DEFAULT_WEB_CALLER_DISABLE_HTTPS, help="If '0', the web caller will use http instead of https. This is unsecure, be careful!")
    ap.add_argument("-HP", "--host_port", required=False, type=int, default=DEFAULT_HOST_PORT, help="Host-Port")
    ap.add_argument("-DEB", "--debug", type=int, choices=range(0, 2), default=DEFAULT_DEBUG, required=False, help="If '1', the application will output additional information")
    ap.add_argument("-CC", "--cert_check", type=int, choices=range(0, 2), default=DEFAULT_CERT_CHECK, required=False, help="If '0', the application won't check any ssl certification")
    ap.add_argument("-MIF", "--mixer_frequency", type=int, required=False, default=DEFAULT_MIXER_FREQUENCY, help="Pygame mixer frequency")
    ap.add_argument("-MIS", "--mixer_size", type=int, required=False, default=DEFAULT_MIXER_SIZE, help="Pygame mixer size")
    ap.add_argument("-MIC", "--mixer_channels", type=int, required=False, default=DEFAULT_MIXER_CHANNELS, help="Pygame mixer channels")
    ap.add_argument("-MIB", "--mixer_buffersize", type=int, required=False, default=DEFAULT_MIXER_BUFFERSIZE, help="Pygame mixer buffersize")
    ap.add_argument("-CRL", "--caller_real_life", type=int, choices=range(0, 2), default=DEFAULT_CALLER_REAL_LIFE, required=False, help="change the Caller behaviour to next gen and more Realistic calls")
    ap.add_argument("-CBS", "--call_blind_support", type=int, choices=range(0, 2), default=DEFAULT_CALL_BLIND_SUPPORT, required=False, help="If '1', the application will call target field and which segment was hit for every dart to help blind players")
    args = vars(ap.parse_args())

    global CALLER
    global RANDOM_CALLER
    global RANDOM_CALLER_GENDER
    global RANDOM_CALLER_LANGUAGE
    global CALL_EVERY_DART
    global CALL_CURRENT_PLAYER
    global CALL_BOT_ACTIONS
    global POSSIBLE_CHECKOUT_CALL
    global POSSIBLE_CHECKOUT_CALL_YOURSELF_ONLY
    
    CALLER_SETTINGS_ARGS = {
        'media_path': str(args['media_path']),
        'media_path_shared': str(args['media_path_shared']),
        'caller': args['caller'],
        'caller_real_life': args['caller_real_life'],
        'caller_volume': args['caller_volume'],
        'random_caller': args['random_caller'],
        'random_caller_language': args['random_caller_language'],
        'random_caller_gender': args['random_caller_gender'],
        'call_current_player': args['call_current_player'],
        'call_bot_actions': args['call_bot_actions'],
        'call_every_dart': args['call_every_dart'],
        'call_every_dart_total_score': args['call_every_dart_total_score'],
        'possible_checkout_call': args['possible_checkout_call'],
        'possible_checkout_call_yourself_only': args['possible_checkout_call_yourself_only'],
        'ambient_sounds': args['ambient_sounds'],
        'ambient_sounds_after_calls': args['ambient_sounds_after_calls'],
        'downloads': args['downloads'],
        'downloads_language': args['downloads_language'],
        'downloads_name': args['downloads_name'],
        'remove_old_voice_packs': args['remove_old_voice_packs'],
        'background_audio_volume': args['background_audio_volume'],
        'local_playback': args['local_playback'],
        'web_caller_disable_https': args['web_caller_disable_https'],
        'host_port': args['host_port'],
        'debug': args['debug'],
        'cert_check': args['cert_check'],
        'mixer_frequency': args['mixer_frequency'],
        'mixer_size': args['mixer_size'],
        'mixer_channels': args['mixer_channels'],
        'mixer_buffersize': args['mixer_buffersize'],
        'call_blind_support': args['call_blind_support']
    }

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
    CALLER_REAL_LIFE = args['caller_real_life']
    RANDOM_CALLER = args['random_caller']    
    RANDOM_CALLER_LANGUAGE = args['random_caller_language'] 
    if RANDOM_CALLER_LANGUAGE < 0: RANDOM_CALLER_LANGUAGE = DEFAULT_RANDOM_CALLER_LANGUAGE
    RANDOM_CALLER_GENDER = args['random_caller_gender'] 
    if RANDOM_CALLER_GENDER < 0: RANDOM_CALLER_GENDER = DEFAULT_RANDOM_CALLER_GENDER
    CALL_CURRENT_PLAYER = args['call_current_player']
    CALL_BOT_ACTIONS = args['call_bot_actions']
    CALL_EVERY_DART = args['call_every_dart']
    CALL_EVERY_DART_TOTAL_SCORE = args['call_every_dart_total_score']
    POSSIBLE_CHECKOUT_CALL = args['possible_checkout_call']
    if POSSIBLE_CHECKOUT_CALL < 0: POSSIBLE_CHECKOUT_CALL = 0
    POSSIBLE_CHECKOUT_CALL_YOURSELF_ONLY = args['possible_checkout_call_yourself_only']
    AMBIENT_SOUNDS = args['ambient_sounds']
    AMBIENT_SOUNDS_AFTER_CALLS = args['ambient_sounds_after_calls']
    DOWNLOADS = args['downloads']
    if DOWNLOADS < 0: DOWNLOADS = DEFAULT_DOWNLOADS
    DOWNLOADS_LANGUAGE = args['downloads_language']
    if DOWNLOADS_LANGUAGE < 0: DOWNLOADS_LANGUAGE = DEFAULT_DOWNLOADS_LANGUAGE
    DOWNLOADS_PATH = DEFAULT_DOWNLOADS_PATH
    DOWNLOADS_NAME = args['downloads_name']
    REMOVE_OLD_VOICE_PACKS = args['remove_old_voice_packs']
    BACKGROUND_AUDIO_VOLUME = args['background_audio_volume']
    LOCAL_PLAYBACK = args['local_playback']
    WEB_DISABLE_HTTPS = args['web_caller_disable_https']
    HOST_PORT = args['host_port']
    DEBUG = args['debug']
    CERT_CHECK = args['cert_check']
    MIXER_FREQUENCY = args['mixer_frequency']
    MIXER_SIZE = args['mixer_size']
    MIXER_CHANNELS = args['mixer_channels']
    MIXER_BUFFERSIZE = args['mixer_buffersize']
    CALL_BLIND_SUPPORT = args['call_blind_support']
    if CALL_BLIND_SUPPORT < 0: CALL_BLIND_SUPPORT = DEFAULT_CALL_BLIND_SUPPORT

    # Lade Client-Credentials basierend auf Konfiguration
    client_id, client_secret = load_client_credentials(DEFAULT_NODEJS_SERVER_URL)
    AUTODARTS_CLIENT_ID = client_id
    AUTODARTS_REALM_NAME = 'autodarts'
    AUTODARTS_CLIENT_SECRET = client_secret


    if DEBUG:
        ppi('Started with following arguments:')
        data_to_mask = {
            "autodarts_email": "email", 
            "autodarts_password": "str",
            "autodarts_board_id": "str"
        }
        masked_args = mask(args, data_to_mask)
        ppi(json.dumps(masked_args, indent=4))
    

    global boardManagerAddress
    boardManagerAddress = None

    global lastMessage
    lastMessage = None

    global lastCorrectThrow
    lastCorrectThrow = None

    global currentMatch
    currentMatch = None

    global matchIsActive
    matchIsActive = False

    global blindSupport
    blindSupport = BlindSupport(
        sound_effect_callback=play_sound_effect,
        enabled=(CALL_BLIND_SUPPORT == 1)
    )

    global match_lock
    match_lock = threading.Lock()

    global currentMatchPlayers
    currentMatchPlayers = []

    global currentMatchHost
    currentMatchHost = None

    global callers_profiles_all
    callers_profiles_all = []

    global caller_profiles_banned
    caller_profiles_banned = []

    global caller_profiles_favoured
    caller_profiles_favoured = []

    global callers_available
    callers_available = []

    global caller
    caller = None

    global caller_title
    caller_title = ''

    global caller_title_without_version
    caller_title_without_version = ''

    global lastPoints
    lastPoints = None

    global isBullingFinished
    isBullingFinished = False

    global isGameFinished
    isGameFinished = False

    global background_audios
    background_audios = None

    global mirror_files
    mirror_files = []

    # Threading Event zum Unterbrechen von wartenden Sound-Schleifen
    global sound_break_event
    sound_break_event = threading.Event()

    global checkoutsCounter
    checkoutsCounter = {}

    global webCallerSyncs
    webCallerSyncs = {}

    global lobbyPlayers
    lobbyPlayers = []

    global gotcha_last_player_points
    gotcha_last_player_points = []

    global oneGoodDart
    oneGoodDart = False

    global bermudaBusted
    bermudaBusted = ''

    global indexNameMacro
    indexNameMacro = {}

    DB_ARGS = {
    "userID": BOARD_OWNER,
    "location": USER_LOCATION,
    "darts_wled": EXT_WLED,
    "darts_pixel": EXT_PIXEL,
    "caller_version": VERSION,
    "wled_version": "",
    "pixel_version": ""
    }

    osType = plat
    osName = os.name
    osRelease = platform.release()
    ppi('\r\n', None, '')
    ppi('##########################################', None, '')
    ppi('       WELCOME TO DARTS-CALLER', None, '')
    ppi('##########################################', None, '')
    ppi('VERSION: ' + VERSION, None, '')
    ppi('RUNNING OS: ' + osType + ' | ' + osName + ' | ' + osRelease, None, '')
    ppi('SUPPORTED GAME-VARIANTS: ' + " ".join(str(x) for x in SUPPORTED_GAME_VARIANTS), None, '')
    ppi('DONATION: bitcoin:bc1q8dcva098rrrq2uqhv38rj5hayzrqywhudvrmxa', None, '')
    ppi('DONATION: paypal:https://paypal.me/I3ull3t', None, '')
    ppi('\r\n', None, '')

    path_status = check_paths(__file__, AUDIO_MEDIA_PATH, AUDIO_MEDIA_PATH_SHARED)
    if path_status is not None: 
        ppi('Please check your arguments: ' + path_status)
        sys.exit()  


    if LOCAL_PLAYBACK:
        try:
            mixer.pre_init(MIXER_FREQUENCY, MIXER_SIZE, MIXER_CHANNELS, MIXER_BUFFERSIZE)
            mixer.init()
        except Exception as e:
            ppe("Failed to initialize audio device! Make sure the target device is connected and configured as os default. Fallback to web-caller", e)

    if plat == 'Windows' and BACKGROUND_AUDIO_VOLUME > 0.0:
        try:
            background_audios = AudioUtilities.GetAllSessions()
            audio_muter = threading.Thread(target=mute_background, args=[BACKGROUND_AUDIO_VOLUME])
            audio_muter.start()
        except Exception as e:
            ppe("Background-Muter failed!", e)

    try:
        load_callers_banned()
    except Exception as e:
        ppe("Load banned voice-packs failed!", e)

    try:
        load_callers_favoured()
    except Exception as e:
        ppe("Load favoured voice-packs failed!", e)

    try: 
        download_callers()
    except Exception as e:
        ppe("Download voice-packs failed", e)

    try:
        delete_old_callers()
    except Exception as e:
        ppe("Delete old voice-packs failed", e)

    try:
        load_callers()
    except Exception as e:
        ppe("Load voice-packs failed!", e)  

    try:
        setup_caller()
        if caller == None:
            ppi('A caller with name "' + str(CALLER) + '" does NOT exist! Please compare your input with list of available voice-packs.')
            sys.exit()  
    except Exception as e:
        ppe("Setup caller failed!", e)
        sys.exit()  

    try:  
        path_to_crt = None
        path_to_key = None
        ssl_context = None
        if WEB_DISABLE_HTTPS == False:
            path_to_crt = os.path.join(AUDIO_MEDIA_PATH, "dummy.crt")
            path_to_key = os.path.join(AUDIO_MEDIA_PATH, "dummy.key")
            if os.path.exists(path_to_crt) and os.path.exists(path_to_key):
                ssl_context = (path_to_crt, path_to_key)
            else:
                ssl_context = make_ssl_devcert(str(AUDIO_MEDIA_PATH / "dummy"), host=DEFAULT_HOST_IP)

        # # Token vom Node.js-Server abrufen
        # credentials = get_keycloak_token(AUTODART_USER_EMAIL, AUTODART_USER_PASSWORD)
        # if not credentials:
        #     print("Authentifizierung fehlgeschlagen. Programm wird beendet.")
        #     sys.exit()

        # Instanz der AutodartsKeycloakClient-Klasse erstellen
        # keycloak_client = AutodartsKeycloakClient(
        #     username=AUTODART_USER_EMAIL,
        #     password=AUTODART_USER_PASSWORD,
        #     client_id=None,
        #     client_secret=None,
        #     debug=True,  # Debugging aktivieren
        #     nodejs_server_url=NODEJS_SERVER_URL
        # )
        # keycloak_client.start()
        # ORIGINAL KEYCLOAK AUTHENTICATION
        kc = AutodartsKeycloakClient(username=AUTODART_USER_EMAIL, 
                                password=AUTODART_USER_PASSWORD, 
                                client_id=AUTODARTS_CLIENT_ID, 
                                client_secret=AUTODARTS_CLIENT_SECRET,
                                debug=DEBUG)                     
        kc.start()
        connect_autodarts()

        start_webserver(DEFAULT_HOST_IP, HOST_PORT, ssl_context)
        # keycloak_client.stop()
        kc.stop()
    except Exception as e:
        ppe("Connect failed: ", e)
