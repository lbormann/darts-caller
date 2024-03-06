import os
import sys
from pathlib import Path
import time
import json
import base64
import platform
import random
import argparse
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
import certifi
import psutil
import queue
from mask import mask
import re
from urllib.parse import quote, unquote
from flask import Flask, render_template, send_from_directory
from autodarts_keycloak_client import AutodartsKeycloakClient

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
main_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(main_directory)


VERSION = '2.10.4'


DEFAULT_EMPTY_PATH = ''
DEFAULT_CALLER_VOLUME = 1.0
DEFAULT_CALLER = None
DEFAULT_RANDOM_CALLER = 1
DEFAULT_RANDOM_CALLER_EACH_LEG = 0
DEFAULT_RANDOM_CALLER_LANGUAGE = 0
DEFAULT_RANDOM_CALLER_GENDER = 0
DEFAULT_CALL_CURRENT_PLAYER = 1
DEFAULT_CALL_CURRENT_PLAYER_ALWAYS = 0
DEFAULT_CALL_EVERY_DART = 0
DEFAULT_CALL_EVERY_DART_SINGLE_FILES = 1
DEFAULT_POSSIBLE_CHECKOUT_CALL = 1
DEFAULT_POSSIBLE_CHECKOUT_CALL_SINGLE_FILES = 0
DEFAULT_POSSIBLE_CHECKOUT_CALL_YOURSELF_ONLY = 0
DEFAULT_AMBIENT_SOUNDS = 0.0
DEFAULT_AMBIENT_SOUNDS_AFTER_CALLS = 0
DEFAULT_DOWNLOADS = True
DEFAULT_DOWNLOADS_LIMIT = 3
DEFAULT_DOWNLOADS_LANGUAGE = 1
DEFAULT_DOWNLOADS_NAME = None
DEFAULT_BACKGROUND_AUDIO_VOLUME = 0.0
DEFAULT_WEB_CALLER = 0
DEFAULT_WEB_CALLER_SCOREBOARD = 0
DEFAULT_WEB_CALLER_PORT = 5000
DEFAULT_HOST_PORT = 8079
DEFAULT_DEBUG = False
DEFAULT_CERT_CHECK = True
DEFAULT_MIXER_FREQUENCY = 44100
DEFAULT_MIXER_SIZE = 32
DEFAULT_MIXER_CHANNELS = 2
DEFAULT_MIXER_BUFFERSIZE = 4096
DEFAULT_DOWNLOADS_PATH = 'caller-downloads-temp'
DEFAULT_CALLERS_BANNED_FILE = 'autodarts-caller-banned.txt'
DEFAULT_HOST_IP = '0.0.0.0'


AUTODART_URL = 'https://autodarts.io'
AUTODART_AUTH_URL = 'https://login.autodarts.io/'
AUTODART_CLIENT_ID = 'wusaaa-caller-for-autodarts'
AUTODART_REALM_NAME = 'autodarts'
AUTODART_CLIENT_SECRET = "4hg5d4fddW7rqgoY8gZ42aMpi2vjLkzf"
AUTODART_LOBBIES_URL = 'https://api.autodarts.io/gs/v0/lobbies/'
AUTODART_MATCHES_URL = 'https://api.autodarts.io/gs/v0/matches/'
AUTODART_BOARDS_URL = 'https://api.autodarts.io/bs/v0/boards/'
AUTODART_USERS_URL = 'https://api.autodarts.io/as/v0/users/'
AUTODART_WEBSOCKET_URL = 'wss://api.autodarts.io/ms/v0/subscribe'

SUPPORTED_SOUND_FORMATS = ['.mp3', '.wav']
SUPPORTED_GAME_VARIANTS = ['X01', 'Cricket', 'Random Checkout', 'ATC']
SUPPORTED_CRICKET_FIELDS = [15, 16, 17, 18, 19, 20, 25]
BOGEY_NUMBERS = [169, 168, 166, 165, 163, 162, 159]
TEMPLATE_FILE_ENCODING = 'utf-8-sig'

CALLER_LANGUAGES = {
    1: ['english', 'en', ],
    2: ['french', 'fr', ],
    3: ['russian', 'ru', ],
    4: ['german', 'de', ],
    5: ['spanish', 'es', ],
    6: ['dutch', 'nl', ],
}
CALLER_GENDERS = {
    1: ['female', 'f'],
    2: ['male', 'm'],
}
CALLER_PROFILES = {
    #------------------------------------------------------------------------------------------------
    # GOOGLE / Cloud TTS
    #------------------------------------------------------------------------------------------------
    # -- fr-FR --
    'fr-FR-Wavenet-E-FEMALE': ('https://add.arnes-design.de/ADC/fr-FR-Wavenet-E-FEMALE-v3.zip', 3),
    'fr-FR-Wavenet-B-MALE': ('https://add.arnes-design.de/ADC/fr-FR-Wavenet-B-MALE-v3.zip', 3),
    # -- ru-RU --
    'ru-RU-Wavenet-E-FEMALE': ('https://add.arnes-design.de/ADC/ru-RU-Wavenet-E-FEMALE-v3.zip', 3),
    'ru-RU-Wavenet-B-MALE': ('https://add.arnes-design.de/ADC/ru-RU-Wavenet-B-MALE-v3.zip', 3),
    # -- de-DE --
    'de-DE-Wavenet-F-FEMALE': ('https://add.arnes-design.de/ADC/de-DE-Wavenet-F-FEMALE-v3.zip', 3),  
    'de-DE-Wavenet-B-MALE': ('https://add.arnes-design.de/ADC/de-DE-Wavenet-B-MALE-v3.zip', 3),
    # -- es-ES --
    'es-ES-Wavenet-C-FEMALE': ('https://add.arnes-design.de/ADC/es-ES-Wavenet-C-FEMALE-v3.zip', 3),  
    'es-ES-Wavenet-B-MALE': ('https://add.arnes-design.de/ADC/es-ES-Wavenet-B-MALE-v3.zip', 3),
    # -- nl-NL --
    'nl-NL-Wavenet-B-MALE': ('https://add.arnes-design.de/ADC/nl-NL-Wavenet-B-MALE-v3.zip', 3),  
    'nl-NL-Wavenet-D-FEMALE': ('https://add.arnes-design.de/ADC/nl-NL-Wavenet-D-FEMALE-v3.zip', 3),
    # -- en-US --
    'en-US-Wavenet-E-FEMALE': ('https://add.arnes-design.de/ADC/en-US-Wavenet-E-FEMALE-v4.zip', 4),
    'en-US-Wavenet-G-FEMALE': ('https://add.arnes-design.de/ADC/en-US-Wavenet-G-FEMALE-v4.zip', 4),
    'en-US-Wavenet-A-MALE': ('https://add.arnes-design.de/ADC/en-US-Wavenet-A-MALE-v4.zip', 4),
    'en-US-Wavenet-H-FEMALE': ('https://add.arnes-design.de/ADC/en-US-Wavenet-H-FEMALE-v4.zip', 4),
    'en-US-Wavenet-I-MALE': ('https://add.arnes-design.de/ADC/en-US-Wavenet-I-MALE-v4.zip', 4),
    'en-US-Wavenet-J-MALE': ('https://add.arnes-design.de/ADC/en-US-Wavenet-J-MALE-v4.zip', 4),
    'en-US-Wavenet-F-FEMALE': ('https://add.arnes-design.de/ADC/en-US-Wavenet-F-FEMALE-v4.zip', 4),

    #------------------------------------------------------------------------------------------------
    # AMAZON / AWS Polly
    #------------------------------------------------------------------------------------------------
    # -- nl-NL --
    'nl-NL-Laura-Female': ('https://add.arnes-design.de/ADC/nl-NL-Laura-Female-v2.zip', 2),
    # -- de-AT --
    'de-AT-Hannah-Female': ('https://add.arnes-design.de/ADC/de-AT-Hannah-Female-v2.zip', 2),
    # -- de-DE --
    'de-DE-Vicki-Female': ('https://add.arnes-design.de/ADC/de-DE-Vicki-Female-v5.zip', 5),  
    'de-DE-Daniel-Male': ('https://add.arnes-design.de/ADC/de-DE-Daniel-Male-v5.zip', 5),
    # -- en-US --
    'en-US-Ivy-Female': ('https://add.arnes-design.de/ADC/en-US-Ivy-Female-v5.zip', 5),
    'en-US-Joey-Male': ('https://add.arnes-design.de/ADC/en-US-Joey-Male-v6.zip', 6),
    'en-US-Joanna-Female': ('https://add.arnes-design.de/ADC/en-US-Joanna-Female-v6.zip', 6),
    'en-US-Matthew-Male': ('https://add.arnes-design.de/ADC/en-US-Matthew-Male-v3.zip', 3),
    'en-US-Danielle-Female': ('https://add.arnes-design.de/ADC/en-US-Danielle-Female-v3.zip', 3),
    'en-US-Kimberly-Female': ('https://add.arnes-design.de/ADC/en-US-Kimberly-Female-v2.zip', 2),
    'en-US-Ruth-Female': ('https://add.arnes-design.de/ADC/en-US-Ruth-Female-v2.zip', 2),
    'en-US-Salli-Female': ('https://add.arnes-design.de/ADC/en-US-Salli-Female-v2.zip', 2),
    'en-US-Kevin-Male': ('https://add.arnes-design.de/ADC/en-US-Kevin-Male-v2.zip', 2),
    'en-US-Justin-Male': ('https://add.arnes-design.de/ADC/en-US-Justin-Male-v2.zip', 2),
    'en-US-Stephen-Male': ('https://add.arnes-design.de/ADC/en-US-Stephen-Male-v5.zip', 5),  
    'en-US-Kendra-Female': ('https://add.arnes-design.de/ADC/en-US-Kendra-Female-v6.zip', 6),
    'en-US-Gregory-Male': ('https://add.arnes-design.de/ADC/en-US-Gregory-Male-v3.zip', 3),
    
    # 'TODONAME': ('TODOLINK', TODOVERSION),  
}
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

WEB_DB_NAME = "ADC1"



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

def check_paths(main_directory, audio_media_path, audio_media_path_shared, blacklist_path):
    try:
        main_directory = get_executable_directory()
        errors = None

        audio_media_path = os.path.normpath(audio_media_path)
        
        if audio_media_path_shared != DEFAULT_EMPTY_PATH:
            audio_media_path_shared = os.path.normpath(audio_media_path_shared)
        if blacklist_path != DEFAULT_EMPTY_PATH:
            blacklist_path = os.path.normpath(blacklist_path)

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

        if blacklist_path != '':
            if same_drive(blacklist_path, main_directory) == True and os.path.commonpath([blacklist_path, main_directory]) == main_directory:
                errors = 'BLACKLIST_FILE_PATH (-BLP) is a subdirectory of MAIN_DIRECTORY. This is NOT allowed.'

    except Exception as e:
        errors = f'Path validation failed: {e}'

    if errors is not None:
        ppi("main_directory: " + main_directory)
        ppi("audio_media_path: " + str(audio_media_path))
        ppi("audio_media_path_shared: " + str(audio_media_path_shared))
        ppi("blacklist_path: " + str(blacklist_path))

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
    if DOWNLOADS:
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
            ppi("Downloader: filter for name: " + str(dl_name))
        else:
            # filter for language
            if DOWNLOADS_LANGUAGE > 0:
                ppi("Downloader: filter for language: " + str(DOWNLOADS_LANGUAGE))
                downloads_filtered = {}
                for speaker_name, speaker_download_url in download_list.items():
                    caller_language_key = grab_caller_language(speaker_name)
                    if caller_language_key != DOWNLOADS_LANGUAGE:
                        continue
                    downloads_filtered[speaker_name] = speaker_download_url
                download_list = downloads_filtered

            # filter for limit
            if DOWNLOADS_LIMIT > 0 and len(download_list) > 0 and DOWNLOADS_LIMIT < len(download_list):
                ppi("Downloader: limit to: " + str(DOWNLOADS_LIMIT))
                download_list = {k: download_list[k] for k in list(download_list.keys())[-DOWNLOADS_LIMIT:]}



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

                ppi("Extracting voice-pack..")

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
                ppi('Voice-pack added: ' + cpr_name)

            except Exception as e:
                ppe('Failed to process voice-pack: ' + cpr_name, e)
            finally:
                shutil.rmtree(DOWNLOADS_PATH, ignore_errors=True)

def ban_caller(only_change):
    global caller_title

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

        if BLACKLIST_PATH != DEFAULT_EMPTY_PATH:
            global caller_profiles_banned
            caller_profiles_banned.append(caller_title)
            path_to_callers_banned_file = os.path.join(BLACKLIST_PATH, DEFAULT_CALLERS_BANNED_FILE)   
            with open(path_to_callers_banned_file, 'w') as bcf:
                for cpb in caller_profiles_banned:
                    bcf.write(cpb.lower() + '\n')

    mirror_sounds()
    setup_caller()

    if play_sound_effect('hi', wait_for_last = False):
        mirror_sounds()
    


def load_callers_banned(preview=False):
    global caller_profiles_banned
    caller_profiles_banned = []
    
    if BLACKLIST_PATH == DEFAULT_EMPTY_PATH:
        return
    
    path_to_callers_banned_file = os.path.join(BLACKLIST_PATH, DEFAULT_CALLERS_BANNED_FILE)
    
    if os.path.exists(path_to_callers_banned_file):
        try:
            with open(path_to_callers_banned_file, 'r') as bcf:
                caller_profiles_banned = list(set(line.strip() for line in bcf))
                if preview:
                    banned_info = f"Banned voice-packs: {len(caller_profiles_banned)} [ - "
                    for cpb in caller_profiles_banned:
                        banned_info += cpb + " - "
                    banned_info += "]"
                    ppi(banned_info)
        except FileExistsError:
            pass
    else:
        # directory = os.path.dirname(path_to_callers_banned_file)
        # os.makedirs(directory, exist_ok=True)
        try:
            with open(path_to_callers_banned_file, 'x'):
                ppi(f"'{path_to_callers_banned_file}' created successfully.")
        except Exception as e:
            ppe(f"Failed to create '{path_to_callers_banned_file}'", e)

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

    load_callers_banned()
        
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

def grab_caller_name(caller_root):
    return os.path.basename(os.path.normpath(caller_root[0])).lower()

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

def filter_most_recent_version(path_list):
    def get_last_component(path):
        return os.path.basename(os.path.normpath(path))

    def is_versioned(entry):
        return bool(re.search(r'-v\d+$', entry))

    def highest_version(base_entry):
        versions = [int(re.search(r'-v(\d+)$', x[0]).group(1)) for x in path_list if base_entry + "-v" in x[0]]
        return max(versions, default=None)

    base_entries = set()
    for item in path_list:
        entry = get_last_component(item[0])
        if not is_versioned(entry):
            base_entries.add(entry)

    filtered_list = []
    for item in path_list:
        entry = get_last_component(item[0])
        base_entry = re.sub(r'-v\d+$', '', entry)
        highest_ver = highest_version(base_entry)
        if highest_ver is not None and entry == base_entry + "-v" + str(highest_ver):
            filtered_list.append(item)
        elif highest_ver is None:
            filtered_list.append(item)
    
    return filtered_list

def setup_caller():
    global caller
    global caller_title
    global caller_title_without_version
    global caller_profiles_banned
    caller = None
    caller_title = ''
    caller_title_without_version = ''

    callers = load_callers()
    ppi(str(len(callers)) + ' voice-pack(s) found.')

    if CALLER != DEFAULT_CALLER and CALLER != '':
        wished_caller = CALLER.lower()
        for c in callers:
            caller_name = os.path.basename(os.path.normpath(c[0])).lower()
            ppi(caller_name, None, '')
            if caller == None and caller_name == wished_caller:
                caller = c

    else:
        for c in callers: 
            caller_name = grab_caller_name(c)
            ppi(caller_name, None, '')

        if RANDOM_CALLER == False:
            caller = callers[0]
        else:
            callers_filtered = []
            for c in callers:
                caller_name = grab_caller_name(c)

                if caller_name in caller_profiles_banned or caller_name.split("-v")[0] in caller_profiles_banned:
                    continue

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
                # reduce to most recent version
                callers_filtered = filter_most_recent_version(callers_filtered)
                caller = random.choice(callers_filtered)

    if(caller != None):
        for sound_file_key, sound_file_values in caller[1].items():
            sound_list = list()
            for sound_file_path in sound_file_values:
                sound_list.append(sound_file_path)
            caller[1][sound_file_key] = sound_list

        caller_title = str(os.path.basename(os.path.normpath(caller[0])))
        caller_title_without_version = caller_title.split("-v")[0].lower()
        ppi("Your current caller: " + caller_title + " knows " + str(len(caller[1].values())) + " Sound-file-key(s)")
        # ppi(caller[1])
        caller = caller[1]


        # files = []
        # for key, value in caller.items():
        #     for sound_file in value:
        #         files.append(quote(sound_file, safe=""))
        # get_event = {
        #     "event": "get",
        #     "caller": caller_title_without_version,
        #     "files": files
        # }
        # if server != None:
        #   broadcast(get_event)

        welcome_event = {
            "event": "welcome",
            "caller": caller_title_without_version,
            "specific": CALLER != DEFAULT_CALLER and CALLER != '',
            "banable": BLACKLIST_PATH != DEFAULT_EMPTY_PATH
        }
        if server != None:
            broadcast(welcome_event)


def play_sound(sound, wait_for_last, volume_mult, mod):
    volume = 1.0
    if AUDIO_CALLER_VOLUME is not None:
        volume = AUDIO_CALLER_VOLUME * volume_mult

    if WEB > 0:
        global mirror_files
        global caller_title_without_version
        
        mirror_file = {
                    "caller": caller_title_without_version,
                    "path": quote(sound, safe=""),
                    "wait": wait_for_last,
                    "volume": volume,
                    "mod": mod
                }
        mirror_files.append(mirror_file)

    if WEB == 0 or WEB == 2:
        if wait_for_last == True:
            while mixer.get_busy():
                time.sleep(0.01)

        s = mixer.Sound(sound)
        s.set_volume(volume)
        s.play()

    ppi('Playing: "' + sound + '"')

def play_sound_effect(sound_file_key, wait_for_last = False, volume_mult = 1.0, mod = True):
    try:
        global caller
        play_sound(random.choice(caller[sound_file_key]), wait_for_last, volume_mult, mod)
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
        res = requests.get(AUTODART_USERS_URL + user_id + "/stats/" + variant + "?limit=" + limit, headers={'Authorization': 'Bearer ' + kc.access_token})
        m = res.json()
        # ppi(m)
        return m['average']['average']
    except Exception as e:
        ppe('Receive player-stats failed', e)
        return None

def next_game():
    if play_sound_effect('control_next_game', wait_for_last = False, volume_mult = 1.0, mod = False) == False:
        play_sound_effect('control', wait_for_last = False, volume_mult = 1.0, mod = False)
    mirror_sounds()

    # post
    # https://api.autodarts.io/gs/v0/matches/<match-id>/games/next
    try:
        global currentMatch
        if currentMatch != None:
            requests.post(AUTODART_MATCHES_URL + currentMatch + "/games/next", headers={'Authorization': 'Bearer ' + kc.access_token})

    except Exception as e:
        ppe('Next game failed', e)

def next_throw():
    if play_sound_effect('control_next', wait_for_last = False, volume_mult = 1.0, mod = False) == False:
        play_sound_effect('control', wait_for_last = False, volume_mult = 1.0, mod = False)
    mirror_sounds()

    # post
    # https://api.autodarts.io/gs/v0/matches/<match-id>/players/next
    try:
        global currentMatch
        if currentMatch != None:
            requests.post(AUTODART_MATCHES_URL + currentMatch + "/players/next", headers={'Authorization': 'Bearer ' + kc.access_token})

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
            requests.post(AUTODART_MATCHES_URL + currentMatch + "/undo", headers={'Authorization': 'Bearer ' + kc.access_token})
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
            requests.patch(AUTODART_MATCHES_URL + currentMatch + "/throws", json=data, headers={'Authorization': 'Bearer ' + kc.access_token})
            lastCorrectThrow = data
        else:
            lastCorrectThrow = None 

    except Exception as e:
        lastCorrectThrow = None 
        ppe('Correcting throw failed', e)

def receive_local_board_address():
    try:
        global boardManagerAddress

        if boardManagerAddress == None:
            res = requests.get(AUTODART_BOARDS_URL + AUTODART_USER_BOARD_ID, headers={'Authorization': 'Bearer ' + kc.access_token})
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

# deprecated
def poll_lobbies(ws):
    def process(*args):
        global currentMatch
        global lobbyPlayers

        while currentMatch == None:
            try:   
                res = requests.get(AUTODART_LOBBIES_URL, headers={'Authorization': 'Bearer ' + kc.access_token})
                res = res.json()
                # ppi(json.dumps(res, indent = 4, sort_keys = True))

                # watchout for a lobby with my board-id
                for m in res:
                    for p in m['players']:
                        if 'boardId' in p and p['boardId'] == AUTODART_USER_BOARD_ID:
                            ppi('Listen to lobby: ' + m['id'])
                            paramsSubscribeLobbyEvents = {
                                    "channel": "autodarts.lobbies",
                                    "type": "subscribe",
                                    "topic": m['id'] + ".state"
                                }
                            ws.send(json.dumps(paramsSubscribeLobbyEvents))
                            paramsSubscribeLobbyEvents = {
                                    "channel": "autodarts.lobbies",
                                    "type": "subscribe",
                                    "topic": m['id'] + ".events"
                                }
                            ws.send(json.dumps(paramsSubscribeLobbyEvents))
                            lobbyPlayers = []

                            if play_sound_effect("lobby_ambient_in", False):
                                mirror_sounds()
                            return
            except Exception as e:
                ppe('Lobby-polling failed: ', e)
            
            ppi('Waiting for lobby or match..')
            time.sleep(5)
    t = threading.Thread(target=process)
    t.start()

def listen_to_match(m, ws):
    global currentMatch
    global currentMatchHost
    global currentMatchPlayers

    # EXAMPLE
    # {
    #     "channel": "autodarts.boards",
    #     "data": {
    #         "event": "start",
    #         "id": "82f917d0-0308-2c27-c4e9-f53ef2e98ad2"
    #     },
    #     "topic": "1ba2df53-9a04-51bc-9a5f-667b2c5f315f.matches"  
    # }

    if 'event' not in m:
        return

    if m['event'] == 'start':
        currentMatch = m['id']
        ppi('Listen to match: ' + currentMatch)


        try:
            setup_caller()
        except Exception as e:
            ppe("Setup callers failed!", e)

        try:
            res = requests.get(AUTODART_MATCHES_URL + currentMatch, headers={'Authorization': 'Bearer ' + kc.access_token})
            m = res.json()
            # ppi(json.dumps(m, indent = 4, sort_keys = True))

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

            if mode != 'Bull-off':
                callPlayerNameState = False
                if CALL_CURRENT_PLAYER and currentPlayerName != None:
                    callPlayerNameState = play_sound_effect(currentPlayerName)

                if play_sound_effect('matchon', callPlayerNameState) == False:
                    play_sound_effect('gameon', callPlayerNameState)

                if AMBIENT_SOUNDS != 0.0 and play_sound_effect('ambient_matchon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                    play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

            mirror_sounds()
            ppi('Matchon')

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
        
    elif m['event'] == 'finish' or m['event'] == 'delete':
        ppi('Stop listening to match: ' + m['id'])

        currentMatchHost = None
        # currentMatchPlayers = None
        currentMatchPlayers = []

        paramsUnsubscribeMatchEvents = {
            "type": "unsubscribe",
            "channel": "autodarts.matches",
            "topic": m['id'] + ".state"
        }
        ws.send(json.dumps(paramsUnsubscribeMatchEvents))

        if m['event'] == 'delete':
            play_sound_effect('matchcancel', mod = False)
            mirror_sounds()

        # poll_lobbies(ws)

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
    
    variant = m['variant']
    players = m['players']
    currentPlayerIndex = m['player']
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

    # ppi('matchon: '+ str(matchon) )
    # ppi('gameon: '+ str(gameon) )
    # ppi('isGameFinished: ' + str(isGameFinished))

    pcc_success = False
    isGameFin = False

    if turns != None and turns['throws'] != []:
        lastPoints = points

    # Darts pulled (Playerchange and Possible-checkout)
    if gameon == False and turns != None and turns['throws'] == [] or isGameFinished == True:
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
                        if CALL_CURRENT_PLAYER:
                            play_sound_effect(currentPlayerName)

                        if POSSIBLE_CHECKOUT_CALL_SINGLE_FILE:
                            pcc_success = play_sound_effect('yr_' + remaining, True)
                            if pcc_success == False:
                                pcc_success = play_sound_effect(remaining, True)
                        else:
                            pcc_success = (play_sound_effect('you_require', True) and play_sound_effect(remaining, True))
                        
                        ppi('Checkout possible: ' + remaining)
                    else:
                        if AMBIENT_SOUNDS != 0.0:
                            play_sound_effect('ambient_bogey_number', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                        ppi('bogey-number: ' + remaining)

            if pcc_success == False and CALL_CURRENT_PLAYER and CALL_CURRENT_PLAYER_ALWAYS and numberOfPlayers > 1:
                play_sound_effect(currentPlayerName)

            # Player-change
            if pcc_success == False and AMBIENT_SOUNDS != 0.0:
                play_sound_effect('ambient_playerchange', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
                

            ppi("Next player")

    # Call every thrown dart
    elif CALL_EVERY_DART == True and turns != None and turns['throws'] != [] and len(turns['throws']) >= 1 and busted == False and matchshot == False and gameshot == False: 

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

        if CALL_CURRENT_PLAYER:
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
            

        if RANDOM_CALLER_EACH_LEG:
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

        if CALL_CURRENT_PLAYER:
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

        if RANDOM_CALLER_EACH_LEG:
            setup_caller()
        ppi('Gameshot')

    # Check for matchon
    elif matchon == True:
        isGameFinished = False

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
            "players": currentMatchPlayers,
            "player": currentPlayerName,
            "game": {
                "mode": variant,
                "pointsStart": str(base),
                # TODO: fix
                "special": "TODO"
                }     
            }
        broadcast(matchStarted)

        callPlayerNameState = False
        if CALL_CURRENT_PLAYER:
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

        reset_checkouts_counter()

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

        callPlayerNameState = False
        if CALL_CURRENT_PLAYER:
            callPlayerNameState = play_sound_effect(currentPlayerName)

        play_sound_effect('gameon', callPlayerNameState, mod = False)

        if AMBIENT_SOUNDS != 0.0:
            if play_sound_effect('ambient_gameon_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False) == False:
                play_sound_effect('ambient_gameon', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

        ppi('Gameon')
          
    # Check for busted turn
    elif busted == True:
        lastPoints = "B"
        isGameFinished = False

        busted = { 
                    "event": "busted",
                    "player": currentPlayerName,
                    "playerIsBot": str(currentPlayerIsBot),
                    "game": {
                        "mode": variant
                    }       
                }
        broadcast(busted)

        play_sound_effect('busted', mod = False)

        if AMBIENT_SOUNDS != 0.0:
            play_sound_effect('ambient_noscore', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)

        ppi('Busted')
    
    # Check for 1. Dart
    elif turns != None and turns['throws'] != [] and len(turns['throws']) == 1:
        isGameFinished = False

    # Check for 2. Dart
    elif turns != None and turns['throws'] != [] and len(turns['throws']) == 2:
        isGameFinished = False

    # Check for 3. Dart - Score-call
    elif turns != None and turns['throws'] != [] and len(turns['throws']) == 3:
        isGameFinished = False

        dartsThrown = {
            "event": "darts-thrown",
            "player": currentPlayerName,
            "playerIsBot": str(currentPlayerIsBot),
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
    if CALL_EVERY_DART and turns != None and turns['throws'] != [] and len(turns['throws']) >= 1: 
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
            if play_sound_effect('ambient_gameshot_' + currentPlayerName, AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False):
                pass
            else:
                play_sound_effect('ambient_gameshot', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
        
        if RANDOM_CALLER_EACH_LEG:
            setup_caller()
        ppi('Gameshot')
    
    # Check for matchon
    elif m['gameScores'][0] == 0 and m['scores'] == None and turns['throws'] == [] and m['round'] == 1 and m['leg'] == 1 and m['set'] == 1:
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
                    "playerIsBot": str(currentPlayerIsBot),
                    "game": {
                        "mode": variant
                    }       
                }
        broadcast(busted)

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
            "playerIsBot": str(currentPlayerIsBot),
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

        if CALL_CURRENT_PLAYER and CALL_CURRENT_PLAYER_ALWAYS:
            play_sound_effect(currentPlayerName)

        if AMBIENT_SOUNDS != 0.0:
            play_sound_effect('ambient_playerchange', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
        
        ppi("Next player")

    mirror_sounds()
    if isGameFin == True:
        isGameFinished = True

def process_match_atc(m):
    global isGameFinished

    variant = m['variant']
    needHits = m['settings']['hits']
    currentPlayerIndex = m['player']
    currentPlayer = m['players'][currentPlayerIndex]
    currentPlayerName = str(currentPlayer['name']).lower()
    numberOfPlayers = len(m['players'])
    isRandomOrder = m['settings']['order'] == 'Random-Bull'

    turns = m['turns'][0]
    matchshot = (m['winner'] != -1 and isGameFinished == False)

    currentTargetsPlayer = m['state']['currentTargets'][currentPlayerIndex]
    currentTarget = m['state']['targets'][currentPlayerIndex][int(currentTargetsPlayer)]

    # weird behavior by the api i guess?
    if currentTarget['count'] == 0 and int(currentTargetsPlayer) > 0 and turns['throws'] != []:
        currentTarget = m['state']['targets'][currentPlayerIndex][int(currentTargetsPlayer) -1]

    if turns is not None and turns['throws']:
        lastThrow = turns['throws'][-1]
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

    if matchshot:
        isGameFinished = True
        matchWon = {
            "event": "match-won",
            "player": currentPlayerName,
            "game": {
                "mode": variant,
                "dartsThrownValue": "0"
            } 
        }
        broadcast(matchWon)

        if play_sound_effect('matchshot') == False:
            play_sound_effect('gameshot')

        if CALL_CURRENT_PLAYER:
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
        play_sound_effect('atc_target_next', True)
        # only call next target number if random order
        if isRandomOrder:
            play_sound_effect(str(m['state']['targets'][currentPlayerIndex][int(currentTargetsPlayer)]['number']), True)

    if turns['throws'] == []:
        play_sound_effect('ambient_playerchange', AMBIENT_SOUNDS_AFTER_CALLS, volume_mult = AMBIENT_SOUNDS, mod = False)
        if CALL_CURRENT_PLAYER and CALL_CURRENT_PLAYER_ALWAYS and numberOfPlayers > 1:
            play_sound_effect(currentPlayerName, True)
    
    mirror_sounds()

def process_bulling(m):
    currentPlayerIndex = m['player']
    currentPlayer = m['players'][currentPlayerIndex]
    currentPlayerName = str(currentPlayer['name']).lower()
    currentPlayerIsBot = (m['players'][currentPlayerIndex]['cpuPPR'] is not None)
    gameshot = m['gameWinner'] != -1

    if gameshot == True:
        bullingEnd = {
            "event": "bulling-end",
            "player": currentPlayerName,
            "playerIsBot": str(currentPlayerIsBot)
        }
        broadcast(bullingEnd)

        name = play_sound_effect((m['players'][m['gameWinner']]['name']).lower())
        if name:
            play_sound_effect('bulling_end', wait_for_last=True)
    else:
        if m['round'] == 1 and m['gameScores'] is None:  
            bullingStart = {
                "event": "bulling-start",
                "player": currentPlayerName,
                "playerIsBot": str(currentPlayerIsBot)
            }
            broadcast(bullingStart)

            play_sound_effect('bulling_start')
        
    mirror_sounds()

def process_common(m):
    broadcast(m)


def connect_autodarts():
    def process(*args):
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(AUTODART_WEBSOCKET_URL,
                                    header={'Authorization': 'Bearer ' + kc.access_token},
                                    on_open = on_open_autodarts,
                                    on_message = on_message_autodarts,
                                    on_error = on_error_autodarts,
                                    on_close = on_close_autodarts)
        

        ws.run_forever()
    threading.Thread(target=process).start()

def on_open_autodarts(ws):
    try:
        res = requests.get(AUTODART_MATCHES_URL, headers={'Authorization': 'Bearer ' + kc.access_token})
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

        ppi('Receiving live information for board-id: ' + AUTODART_USER_BOARD_ID)
        # poll_lobbies(ws)

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
            global lastMessage
            global lobbyPlayers
            m = json.loads(message)
            # ppi(json.dumps(m, indent = 4, sort_keys = True))
  
            if m['channel'] == 'autodarts.matches':
                data = m['data']
                # ppi(json.dumps(data, indent = 4, sort_keys = True))

                global currentMatch
                # ppi('Current Match: ' + currentMatch)
                
                if('turns' in data and len(data['turns']) >=1):
                    data['turns'][0].pop("id", None)
                    data['turns'][0].pop("createdAt", None)

                if lastMessage != data and currentMatch != None and 'id' in data and data['id'] == currentMatch:
                    lastMessage = data

                    # ppi(json.dumps(data, indent = 4, sort_keys = True))

                    process_common(data)

                    variant = data['variant']
                    
                    if variant == 'Bull-off':
                        process_bulling(data)

                    elif variant == 'X01' or variant == 'Random Checkout':
                        process_match_x01(data)
                        
                    elif variant == 'Cricket':
                        process_match_cricket(data)
                    
                    elif variant == 'ATC':
                        process_match_atc(data)

            elif m['channel'] == 'autodarts.boards':
                data = m['data']
                # ppi(json.dumps(data, indent = 4, sort_keys = True))

                listen_to_match(data, ws)
            
            elif m['channel'] == 'autodarts.users':
                data = m['data']
                # ppi(json.dumps(data, indent = 4, sort_keys = True))
                if 'event' in data:
                    if data['event'] == 'lobby-enter':
                        # ppi("lobby-enter", data)

                        lobby_id = data['body']['id']

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

                        if play_sound_effect("lobby_ambient_in", False, mod = False):
                            mirror_sounds()

                    elif data['event'] == 'lobby-leave':
                        # ppi("lobby-leave", data)

                        lobby_id = data['body']['id']

                        ppi('Stop Listen to lobby: ' + lobby_id)
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

                        if play_sound_effect("lobby_ambient_out", False, mod = False):
                            mirror_sounds()

            elif m['channel'] == 'autodarts.lobbies':
                data = m['data']
                # ppi(json.dumps(data, indent = 4, sort_keys = True))
                
                if 'event' in data:
                    if data['event'] == 'start':
                        pass

                    elif data['event'] == 'finish' or data['event'] == 'delete':
                        ppi('Stop listening to lobby: ' + m['id'])
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
                        if play_sound_effect("lobby_ambient_out", False, mod = False):
                            mirror_sounds()
  
                        # poll_lobbies(ws)


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
                        if play_sound_effect("lobby_ambient_out", False, mod = False):
                            mirror_sounds()
                        lobbyPlayers = []
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
                        state = play_sound_effect(player_name, True)
                        if state == False:
                            state = play_sound_effect('player', True)
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
                            # data['variant'].lower()
                            player_avg = get_player_average(player_id)
                            if player_avg != None:
                                player_avg = str(math.ceil(player_avg))
                            ppi(player_name + " (" + player_avg + " average) joined the lobby")

                            state = False
                            state = play_sound_effect(player_name, True)
                            if state == False:
                                state = play_sound_effect('player', True)
                                
                            if player_avg != None and play_sound_effect('average', True):
                                play_sound_effect(player_avg, True)

                            playerJoined = {
                                "event": "lobby",
                                "action": "player-joined",
                                "player": player_name,
                                "average": player_avg
                            }
                            broadcast(playerJoined)
                                    
                            # play_sound_effect('joined', state, True)
                            break
                    mirror_sounds()
            
            else:
                ppi('INFO: unexpected ws-message')
                # ppi(json.dumps(m, indent = 4, sort_keys = True))
                

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
    global webCallerSyncs
    ppi('NEW CLIENT CONNECTED: ' + str(client))
    cid = str(client['id'])
    if cid not in webCallerSyncs or webCallerSyncs[cid] is None:
        webCallerSyncs[cid] = queue.Queue()

def on_message_client(client, server, message):
    def process(*args):
        try:
            global RANDOM_CALLER_LANGUAGE
            global RANDOM_CALLER_GENDER

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
                        ppi('This message is not supported')  
                else:
                    ppi('Can not change board-state as board-address is unknown!')  

            elif message.startswith('correct'):
                msg_splitted = message.split(':')
                msg_splitted.pop(0)
                throw_indices = msg_splitted[:-1]
                score = msg_splitted[len(msg_splitted) - 1]
                correct_throw(throw_indices, score)
                    
            elif message.startswith('next'):
                if message.startswith('next-game'):
                    next_game()
                else:
                    next_throw()

            elif message.startswith('undo'):
                undo_throw()

            elif message.startswith('ban'):
                msg_splitted = message.split(':')
                if len(msg_splitted) > 1:
                    ban_caller(True)
                else:
                    ban_caller(False)

            elif message.startswith('language'):
                msg_splitted = message.split(':')
                if len(msg_splitted) > 1:
                    RANDOM_CALLER_LANGUAGE = int(msg_splitted[1])
                    setup_caller()
                    if play_sound_effect('hi', wait_for_last = False):
                        mirror_sounds()

            elif message.startswith('gender'):
                msg_splitted = message.split(':')
                if len(msg_splitted) > 1:
                    RANDOM_CALLER_GENDER = int(msg_splitted[1])
                    setup_caller()
                    if play_sound_effect('hi', wait_for_last = False):
                        mirror_sounds()

            elif message.startswith('call'):
                msg_splitted = message.split(':')
                to_call = msg_splitted[1]
                call_parts = to_call.split(' ')
                for cp in call_parts:
                    play_sound_effect(cp, wait_for_last = False, volume_mult = 1.0)
                mirror_sounds()

            # elif message.startswith('get'):
            #     files = []
            #     for key, value in caller.items():
            #         for sound_file in value:
            #             files.append(quote(sound_file, safe=""))
            #     get_event = {
            #         "event": "get",
            #         "caller": caller_title_without_version,
            #         "specific": CALLER != DEFAULT_CALLER and CALLER != '',
            #         "banable": BLACKLIST_PATH != DEFAULT_EMPTY_PATH
            #         "files": files
            #     }
            #     unicast(client, get_event)

            elif message.startswith('hello'):
                welcome_event = {
                    "event": "welcome",
                    "caller": caller_title_without_version,
                    "specific": CALLER != DEFAULT_CALLER and CALLER != '',
                    "banable": BLACKLIST_PATH != DEFAULT_EMPTY_PATH
                }
                unicast(client, welcome_event)

            elif message.startswith('sync|'): 
                exists = message[len("sync|"):].split("|")

                # new = []
                # count_exists = 0
                # count_new = 0
                # caller_copied = caller.copy()
                # for key, value in caller_copied.items():
                #     for sound_file in value:
                #         base_name = os.path.basename(sound_file)
                #         if base_name not in exists:
                #             count_new+=1
                #             # ppi("exists: " + base_name)

                #             with open(sound_file, 'rb') as file:
                #                 encoded_file = (base64.b64encode(file.read())).decode('ascii')
                #             # print(encoded_file)
                                
                #             new.append({"name": base_name, "path": quote(sound_file, safe=""), "file": encoded_file})
                #         else:
                #             count_exists+=1
                #             # ppi("new: " + base_name)   
                                
                # ppi(f"Sync {count_new} new files")
                new = [{"name": os.path.basename(sound_file), "path": quote(sound_file, safe=""), "file": (base64.b64encode(open(sound_file, 'rb').read())).decode('ascii')} for key, value in caller.items() for sound_file in value if os.path.basename(sound_file) not in exists]

                res = {
                    'caller': caller_title_without_version,
                    'event': 'sync',
                    'exists': new
                }
                unicast(client, res, dump=True)

            # else try to read json
            else: 
                messageJson = json.loads(message)

                # client requests for sync
                if 'event' in messageJson and messageJson['event'] == 'sync' and caller is not None:                    
                    if 'parted' in messageJson:
                        cid = str(client['id'])

                        # ppi("client-id: " + cid)
                        # ppi("client parted " + str(messageJson['parted']) + " - " + str(messageJson['exists']))   
                        # ppi("client already cached: " + str(len(webCallerSyncs[cid])))             
                    
                        webCallerSyncs[cid].put(messageJson['exists'])

                        partsNeeded = messageJson['parted']
                        # ppi("Sync chunks. parts needed: " + str(partsNeeded))
                        
                        existing = []
                        if webCallerSyncs[cid].qsize() == partsNeeded:
                            while partsNeeded > 0:
                                partsNeeded -= 1
                                existing += webCallerSyncs[cid].get()
                            webCallerSyncs[cid].task_done()
                        else:
                            return
                        
                        new = []
                        count_exists = 0
                        count_new = 0
                        caller_copied = caller.copy()
                        for key, value in caller_copied.items():
                            for sound_file in value:
                                base_name = os.path.basename(sound_file)
                                if base_name not in existing:
                                    count_new += 1
                                    # ppi("new: " + base_name)

                                    with open(sound_file, 'rb') as file:
                                        encoded_file = (base64.b64encode(file.read())).decode('ascii')
                                    # print(encoded_file)
                                        
                                    new.append({"name": base_name, "path": quote(sound_file, safe=""), "file": encoded_file})
                                else:
                                    count_exists+=1
                                    # ppi("exists: " + base_name)   
                                        
                        ppi(f"Sync chunks. {count_new} new files")

                        # new = [{"name": os.path.basename(sound_file), "path": quote(sound_file, safe=""), "file": (base64.b64encode(open(sound_file, 'rb').read())).decode('ascii')} for key, value in caller.items() for sound_file in value if os.path.basename(sound_file) not in webCallerSyncs[cid]]  
                        messageJson['exists'] = new
                        unicast(client, messageJson, dump=True)
                        webCallerSyncs[cid] = queue.Queue()
                    else:
                        # ppi("client already cached: " + str(len(messageJson['exists'])))
                        new = [{"name": os.path.basename(sound_file), "path": quote(sound_file, safe=""), "file": (base64.b64encode(open(sound_file, 'rb').read())).decode('ascii')} for key, value in caller.items() for sound_file in value if os.path.basename(sound_file) not in messageJson['exists']]
                        messageJson['exists'] = new
                        unicast(client, messageJson, dump=True)

        except Exception as e:
            ppe('WS-Client-Message failed.', e)

    t = threading.Thread(target=process).start()

def on_left_client(client, server):
    ppi('CLIENT DISCONNECTED: ' + str(client))
    cid = str(client['id'])
    webCallerSyncs[cid] = None

def broadcast(data):
    def process(*args):
        global server
        server.send_message_to_all(json.dumps(data, indent=2).encode('utf-8'))
    t = threading.Thread(target=process)
    t.start()
    # t.join()

def unicast(client, data, dump=True):
    def process(*args):
        global server
        send_data = data
        if dump:
            send_data = json.dumps(send_data, indent=2).encode('utf-8')
        server.send_message(client, send_data)
    t = threading.Thread(target=process)
    t.start()
    # t.join()



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
    return render_template('index.html', host=DEFAULT_HOST_IP, 
                           app_version=VERSION, 
                           db_name=WEB_DB_NAME, 
                           ws_port=HOST_PORT, 
                           state=WEB, 
                           id=currentMatch,
                           me=AUTODART_USER_BOARD_ID,
                           meHost=currentMatchHost,
                           players=currentMatchPlayers,
                           languages=CALLER_LANGUAGES, 
                           genders=CALLER_GENDERS,
                           language=RANDOM_CALLER_LANGUAGE,
                           gender=RANDOM_CALLER_GENDER
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

@app.route('/scoreboard')
def scoreboard():
    return render_template('scoreboard.html', host=DEFAULT_HOST_IP, ws_port=HOST_PORT, state=WEB_SCOREBOARD)



def start_websocket_server(host, port):
    global server
    server = WebsocketServer(host=host, port=port, loglevel=logging.ERROR)
    server.set_fn_new_client(on_open_client)
    server.set_fn_client_left(on_left_client)
    server.set_fn_message_received(on_message_client)
    server.run_forever()

def start_flask_app(host, port):
    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    check_already_running()
        
    ap = argparse.ArgumentParser()
    
    ap.add_argument("-U", "--autodarts_email", required=True, help="Registered email address at " + AUTODART_URL)
    ap.add_argument("-P", "--autodarts_password", required=True, help="Registered password address at " + AUTODART_URL)
    ap.add_argument("-B", "--autodarts_board_id", required=True, help="Registered board-id at " + AUTODART_URL)
    ap.add_argument("-M", "--media_path", required=True, help="Absolute path to your media")
    ap.add_argument("-MS", "--media_path_shared", required=False, default=DEFAULT_EMPTY_PATH, help="Absolute path to shared media folder (every caller get sounds)")
    ap.add_argument("-V", "--caller_volume", type=float, default=DEFAULT_CALLER_VOLUME, required=False, help="Sets calling-volume between 0.0 (silent) and 1.0 (max)")
    ap.add_argument("-C", "--caller", default=DEFAULT_CALLER, required=False, help="Sets a specific caller (voice-pack) for calling")
    ap.add_argument("-R", "--random_caller", type=int, choices=range(0, 2), default=DEFAULT_RANDOM_CALLER, required=False, help="If '1', the application will randomly choose a caller each game. It only works when your base-media-folder has subfolders with its files")
    ap.add_argument("-L", "--random_caller_each_leg", type=int, choices=range(0, 2), default=DEFAULT_RANDOM_CALLER_EACH_LEG, required=False, help="If '1', the application will randomly choose a caller each leg instead of each game. It only works when 'random_caller=1'")
    ap.add_argument("-RL", "--random_caller_language", type=int, choices=range(0, len(CALLER_LANGUAGES) + 1), default=DEFAULT_RANDOM_CALLER_LANGUAGE, required=False, help="If '0', the application will allow every language.., else it will limit caller selection by specific language")
    ap.add_argument("-RG", "--random_caller_gender", type=int, choices=range(0, len(CALLER_GENDERS) + 1), default=DEFAULT_RANDOM_CALLER_GENDER, required=False, help="If '0', the application will allow every gender.., else it will limit caller selection by specific gender")
    ap.add_argument("-CCP", "--call_current_player", type=int, choices=range(0, 2), default=DEFAULT_CALL_CURRENT_PLAYER, required=False, help="If '1', the application will call who is the current player to throw")
    ap.add_argument("-CCPA", "--call_current_player_always", type=int, choices=range(0, 2), default=DEFAULT_CALL_CURRENT_PLAYER_ALWAYS, required=False, help="If '1', the application will call every playerchange")
    ap.add_argument("-E", "--call_every_dart", type=int, choices=range(0, 2), default=DEFAULT_CALL_EVERY_DART, required=False, help="If '1', the application will call every thrown dart")
    ap.add_argument("-ESF", "--call_every_dart_single_files", type=int, choices=range(0, 2), default=DEFAULT_CALL_EVERY_DART_SINGLE_FILES, required=False, help="If '1', the application will call a every dart by using single, dou.., else it uses two separated sounds: single + x (score)")
    ap.add_argument("-PCC", "--possible_checkout_call", type=int, default=DEFAULT_POSSIBLE_CHECKOUT_CALL, required=False, help="If '1', the application will call a possible checkout starting at 170")
    ap.add_argument("-PCCSF", "--possible_checkout_call_single_files", type=int, choices=range(0, 2), default=DEFAULT_POSSIBLE_CHECKOUT_CALL_SINGLE_FILES, required=False, help="If '1', the application will call a possible checkout by using yr_2-yr_170, else it uses two separated sounds: you_require + x")
    ap.add_argument("-PCCYO", "--possible_checkout_call_yourself_only", type=int, choices=range(0, 2), default=DEFAULT_POSSIBLE_CHECKOUT_CALL_YOURSELF_ONLY, required=False, help="If '1' the caller will only call if there is a checkout possibility if the current player is you")
    ap.add_argument("-A", "--ambient_sounds", type=float, default=DEFAULT_AMBIENT_SOUNDS, required=False, help="If > '0.0' (volume), the application will call a ambient_*-Sounds")
    ap.add_argument("-AAC", "--ambient_sounds_after_calls", type=int, choices=range(0, 2), default=DEFAULT_AMBIENT_SOUNDS_AFTER_CALLS, required=False, help="If '1', the ambient sounds will appear after calling is finished") 
    ap.add_argument("-DL", "--downloads", type=int, choices=range(0, 2), default=DEFAULT_DOWNLOADS, required=False, help="If '1', the application will try to download a curated list of caller-voices")
    ap.add_argument("-DLL", "--downloads_limit", type=int, default=DEFAULT_DOWNLOADS_LIMIT, required=False, help="If '1', the application will try to download a only the X newest caller-voices. -DLN needs to be activated.")
    ap.add_argument("-DLLA", "--downloads_language", type=int, choices=range(0, len(CALLER_LANGUAGES) + 1), default=DEFAULT_DOWNLOADS_LANGUAGE, required=False, help="If '0', the application will download speakers of every language.., else it will limit speaker downloads by specific language")
    ap.add_argument("-DLN", "--downloads_name", default=DEFAULT_DOWNLOADS_NAME, required=False, help="Sets a specific caller (voice-pack) for download")
    ap.add_argument("-BLP", "--blacklist_path", required=False, default=DEFAULT_EMPTY_PATH, help="Absolute path to storage directory for blacklist-file")
    ap.add_argument("-BAV","--background_audio_volume", required=False, type=float, default=DEFAULT_BACKGROUND_AUDIO_VOLUME, help="Set background-audio-volume between 0.1 (silent) and 1.0 (no mute)")
    ap.add_argument("-WEB", "--web_caller", required=False, type=int, choices=range(0, 3), default=DEFAULT_WEB_CALLER, help="If '1' the application will host an web-endpoint, '2' it will do '1' and default caller-functionality.")
    ap.add_argument("-WEBSB", "--web_caller_scoreboard", required=False, type=int, choices=range(0, 2), default=DEFAULT_WEB_CALLER_SCOREBOARD, help="If '1' the application will host an web-endpoint, right to web-caller-functionality.")
    ap.add_argument("-WEBP", "--web_caller_port", required=False, type=int, default=DEFAULT_WEB_CALLER_PORT, help="Web-Caller-Port")
    ap.add_argument("-HP", "--host_port", required=False, type=int, default=DEFAULT_HOST_PORT, help="Host-Port")
    ap.add_argument("-DEB", "--debug", type=int, choices=range(0, 2), default=DEFAULT_DEBUG, required=False, help="If '1', the application will output additional information")
    ap.add_argument("-CC", "--cert_check", type=int, choices=range(0, 2), default=DEFAULT_CERT_CHECK, required=False, help="If '0', the application won't check any ssl certification")
    ap.add_argument("-MIF", "--mixer_frequency", type=int, required=False, default=DEFAULT_MIXER_FREQUENCY, help="Pygame mixer frequency")
    ap.add_argument("-MIS", "--mixer_size", type=int, required=False, default=DEFAULT_MIXER_SIZE, help="Pygame mixer size")
    ap.add_argument("-MIC", "--mixer_channels", type=int, required=False, default=DEFAULT_MIXER_CHANNELS, help="Pygame mixer channels")
    ap.add_argument("-MIB", "--mixer_buffersize", type=int, required=False, default=DEFAULT_MIXER_BUFFERSIZE, help="Pygame mixer buffersize")
    
    args = vars(ap.parse_args())

    global RANDOM_CALLER_GENDER
    global RANDOM_CALLER_LANGUAGE
    
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
    RANDOM_CALLER_LANGUAGE = args['random_caller_language'] 
    if RANDOM_CALLER_LANGUAGE < 0: RANDOM_CALLER_LANGUAGE = DEFAULT_RANDOM_CALLER_LANGUAGE
    RANDOM_CALLER_GENDER = args['random_caller_gender'] 
    if RANDOM_CALLER_GENDER < 0: RANDOM_CALLER_GENDER = DEFAULT_RANDOM_CALLER_GENDER
    CALL_CURRENT_PLAYER = args['call_current_player']
    CALL_CURRENT_PLAYER_ALWAYS = args['call_current_player_always']
    CALL_EVERY_DART = args['call_every_dart']
    CALL_EVERY_DART_SINGLE_FILE = args['call_every_dart_single_files']
    POSSIBLE_CHECKOUT_CALL = args['possible_checkout_call']
    if POSSIBLE_CHECKOUT_CALL < 0: POSSIBLE_CHECKOUT_CALL = 0
    POSSIBLE_CHECKOUT_CALL_SINGLE_FILE = args['possible_checkout_call_single_files']
    POSSIBLE_CHECKOUT_CALL_YOURSELF_ONLY = args['possible_checkout_call_yourself_only']
    AMBIENT_SOUNDS = args['ambient_sounds']
    AMBIENT_SOUNDS_AFTER_CALLS = args['ambient_sounds_after_calls']
    DOWNLOADS = args['downloads']
    DOWNLOADS_LANGUAGE = args['downloads_language']
    if DOWNLOADS_LANGUAGE < 0: DOWNLOADS_LANGUAGE = DEFAULT_DOWNLOADS_LANGUAGE
    DOWNLOADS_LIMIT = args['downloads_limit']
    if DOWNLOADS_LIMIT < 0: DOWNLOADS_LIMIT = DEFAULT_DOWNLOADS_LIMIT
    DOWNLOADS_PATH = DEFAULT_DOWNLOADS_PATH
    DOWNLOADS_NAME = args['downloads_name']
    if args['blacklist_path'] != DEFAULT_EMPTY_PATH:
        BLACKLIST_PATH = Path(args['blacklist_path'])
    else:
        BLACKLIST_PATH = DEFAULT_EMPTY_PATH
    BACKGROUND_AUDIO_VOLUME = args['background_audio_volume']
    WEB = args['web_caller']
    WEB_SCOREBOARD = args['web_caller_scoreboard']
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
        data_to_mask = {
            "autodarts_email": "email", 
            "autodarts_password": "str",
            "autodarts_board_id": "str"
        }
        masked_args = mask(args, data_to_mask)
        ppi(json.dumps(masked_args, indent=4))
    
    
    global server
    server = None

    global boardManagerAddress
    boardManagerAddress = None

    global lastMessage
    lastMessage = None

    global lastCorrectThrow
    lastCorrectThrow = None

    global currentMatch
    currentMatch = None

    global currentMatchPlayers
    currentMatchPlayers = []

    global currentMatchHost
    currentMatchHost = None

    global caller
    caller = None

    global caller_title
    caller_title = ''

    global caller_title_without_version
    caller_title_without_version = ''

    global caller_profiles_banned
    caller_profiles_banned = []

    global lastPoints
    lastPoints = None

    global isGameFinished
    isGameFinished = False

    global background_audios
    background_audios = None

    global mirror_files
    mirror_files = []

    global checkoutsCounter
    checkoutsCounter = {}

    global webCallerSyncs
    webCallerSyncs = {}

    global lobbyPlayers
    lobbyPlayers = []



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
    ppi('DONATION: bitcoin:bc1q8dcva098rrrq2uqhv38rj5hayzrqywhudvrmxa', None, '')
    ppi('\r\n', None, '')

    if CERT_CHECK:
        ssl._create_default_https_context = ssl.create_default_context
    else:
        ssl._create_default_https_context = ssl._create_unverified_context
        os.environ['PYTHONHTTPSVERIFY'] = '0'
        ppi("WARNING: SSL-cert-verification disabled!")

    if WEB == 0 or WEB == 2:
        try:
            mixer.pre_init(MIXER_FREQUENCY, MIXER_SIZE, MIXER_CHANNELS, MIXER_BUFFERSIZE)
            mixer.init()
        except Exception as e:
            WEB = 1
            ppe("Failed to initialize audio device! Make sure the target device is connected and configured as os default. Fallback to web-caller", e)
            # sys.exit()  

    path_status = check_paths(__file__, AUDIO_MEDIA_PATH, AUDIO_MEDIA_PATH_SHARED, BLACKLIST_PATH)
    if path_status is not None: 
        ppi('Please check your arguments: ' + path_status)
        sys.exit()  
    

    if plat == 'Windows' and BACKGROUND_AUDIO_VOLUME > 0.0:
        try:
            background_audios = AudioUtilities.GetAllSessions()
            audio_muter = threading.Thread(target=mute_background, args=[BACKGROUND_AUDIO_VOLUME])
            audio_muter.start()
        except Exception as e:
            ppe("Background-Muter failed!", e)

    try:
        load_callers_banned(preview = True)
        download_callers()
    except Exception as e:
        ppe("Voice-pack fetching failed!", e)

    try:
        setup_caller()
        if caller == None:
            ppi('A caller with name "' + str(CALLER) + '" does NOT exist! Please compare your input with list of available voice-packs.')
            sys.exit()  
    except Exception as e:
        ppe("Setup caller failed!", e)
        sys.exit()  

    try:  
        websocket_server_thread = threading.Thread(target=start_websocket_server, args=(DEFAULT_HOST_IP, HOST_PORT))
        websocket_server_thread.start()

        kc = AutodartsKeycloakClient(username=AUTODART_USER_EMAIL, 
                                     password=AUTODART_USER_PASSWORD, 
                                     client_id=AUTODART_CLIENT_ID, 
                                     client_secret=AUTODART_CLIENT_SECRET,
                                     debug=DEBUG
                                     )
        kc.start()

        if WEB > 0 or WEB_SCOREBOARD:
            # WEB_HOST = get_local_ip_address()
            flask_app_thread = threading.Thread(target=start_flask_app, args=(DEFAULT_HOST_IP, WEB_PORT))
            flask_app_thread.start()

        connect_autodarts()

        websocket_server_thread.join()

        if WEB > 0 or WEB_SCOREBOARD:
            flask_app_thread.join() 

        kc.stop()
    except Exception as e:
        ppe("Connect failed: ", e)
   
