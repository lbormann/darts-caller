import os
import sys
import requests
import logging
from pathlib import Path
from dotenv import load_dotenv

# Version
VERSION = '2.19.1'

# Default Server URL
DEFAULT_NODEJS_SERVER_URL = "http://login-darts-caller.peschi.org:3006"

# Logger setup
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
sh.setFormatter(formatter)
logger = logging.getLogger()
if not logger.handlers:
    logger.setLevel(logging.INFO)
    logger.addHandler(sh)

def ppi(message, info_object=None, prefix='\r\n'):
    logger.info(prefix + str(message))
    if info_object is not None:
        logger.info(str(info_object))

def get_client_credentials_from_nodejs_server(server_url="http://localhost:3006"):
    try:
        url = f"{server_url}/client-credentials"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        credentials = response.json()
        return credentials.get("client_id"), credentials.get("client_secret")
    except Exception as e:
        ppi('\r\n', None, '')
        ppi('########################################################', None, '')
        ppi('               WELCOME TO DARTS-CALLER', None, '')
        ppi('########################################################', None, '')
        ppi('VERSION: ' + VERSION, None, '')
        ppi('DONATION: bitcoin:bc1q8dcva098rrrq2uqhv38rj5hayzrqywhudvrmxa', None, '')
        ppi('DONATION: paypal:https://paypal.me/I3ull3t', None, '')
        ppi('########################################################', None, '')
        ppi('!                                                      !', None, '')
        ppi('!       Credential Server seems to be Offline          !', None, '')
        ppi('!     Contact I3uLL3t at Discord to get support        !', None, '')
        ppi('!                                                      !', None, '')
        ppi('!      IT IS NOT AN AUTODARTS ISSUE!!!!!!!!!!!         !', None, '')
        ppi('########################################################', None, '')
        exit(0)
        return None, None

def load_client_credentials(nodejs_server_url=DEFAULT_NODEJS_SERVER_URL):
    # Prüfe, ob das Programm als One-File-Build ausgeführt wird
    is_one_file_build = hasattr(sys, "_MEIPASS")
    
    if is_one_file_build:
        # Pfad zur extrahierten .env-Datei
        env_path = Path(sys._MEIPASS) / ".env/.env"
    else:
        # Lokaler Pfad für Entwicklungsumgebungen
        env_path = Path(".env")
    
    # Prüfe, ob .env-Datei existiert
    env_file_exists = env_path.exists()
    
    client_id = None
    client_secret = None
    
    if env_file_exists:
        load_dotenv(dotenv_path=env_path)
        client_id = os.getenv("AUTODARTS_CLIENT_ID")
        client_secret = os.getenv("AUTODARTS_CLIENT_SECRET")
    
    # Falls .env-Datei nicht existiert oder als One-File-Build läuft und keine Credentials vorhanden sind
    if (not env_file_exists or is_one_file_build) and (not client_id or not client_secret):
        # print("Keine .env-Datei gefunden oder One-File-Build erkannt. Versuche Client-Credentials vom Server abzurufen...")
        nodejs_client_id, nodejs_client_secret = get_client_credentials_from_nodejs_server(nodejs_server_url)
        
        if nodejs_client_id and nodejs_client_secret:
            # print("Client-Credentials erfolgreich vom Server abgerufen.")
            client_id = nodejs_client_id
            client_secret = nodejs_client_secret
        else:
            ppi('\r\n', None, '')
            ppi('########################################################', None, '')
            ppi('               WELCOME TO DARTS-CALLER', None, '')
            ppi('########################################################', None, '')
            ppi('VERSION: ' + VERSION, None, '')
            ppi('DONATION: bitcoin:bc1q8dcva098rrrq2uqhv38rj5hayzrqywhudvrmxa', None, '')
            ppi('DONATION: paypal:https://paypal.me/I3ull3t', None, '')
            ppi('########################################################', None, '')
            ppi('!                                                      !', None, '')
            ppi('!       Credential Server seems to be Offline          !', None, '')
            ppi('!     Contact I3uLL3t at Discord to get support        !', None, '')
            ppi('!                                                      !', None, '')
            ppi('!      IT IS NOT AN AUTODARTS ISSUE!!!!!!!!!!!         !', None, '')
            ppi('########################################################', None, '')
            exit(0)
    
    return client_id, client_secret
