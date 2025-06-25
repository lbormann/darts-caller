from datetime import datetime, timedelta
from time import sleep
import requests
import threading


class AutodartsKeycloakClient:
    token_lifetime_fraction = 0.9
    tick: int = 3
    run: bool = True
    username: str = None
    password: str = None
    debug: bool = False
    access_token: str = None
    refresh_token: str = None
    user_id: str = None
    expires_at: datetime = None
    refresh_expires_at: datetime = None
    t: threading.Thread = None
    nodejs_server_url: str = None

    def __init__(self, *, username: str, password: str, client_id: str, client_secret: str = None, debug: bool = False, nodejs_server_url: str = "http://localhost:3006"):
        self.username = username
        self.password = password
        self.debug = debug
        self.nodejs_server_url = nodejs_server_url

        self.__get_token()
        self.user_id = self.__get_user_id()

    def __set_token(self, token: dict):
        self.access_token = token['access_token']
        self.refresh_token = token['refresh_token']
        self.expires_at = datetime.now() + timedelta(
            seconds=int(self.token_lifetime_fraction * token["expires_in"])
        )
        self.refresh_expires_at = datetime.now() + timedelta(
            seconds=int(self.token_lifetime_fraction * token["refresh_expires_in"])
        )

    def __get_token(self):
        try:
            url = f"{self.nodejs_server_url}/auth"
            payload = {
                "username": self.username,
                "password": self.password,
                "realm": "autodarts"
            }
            if self.debug:
                print(f"Requesting token from Node.js server: {url} with payload: {payload}")
            response = requests.post(url, json=payload)
            response.raise_for_status()
            token = response.json()
            self.__set_token(token)
            if self.debug:
                # print("Token received:", token)
                print("Token received, expires in: " + str(token['expires_in']) + " seconds")
        except Exception as e:
            print(f"Failed to get token: {e}")
            self.access_token = None

    def __refresh_token(self):
        try:
            url = f"{self.nodejs_server_url}/refresh"
            payload = {
                "refresh_token": self.refresh_token
            }
            if self.debug:
                print(f"Requesting token refresh from Node.js server: {url} with payload: {payload}")
            response = requests.post(url, json=payload)
            response.raise_for_status()
            token = response.json()
            self.__set_token(token)
            if self.debug:
                # print("Token refreshed:", token)
                print("Token refreshed, expires in: " + str(token['expires_in']) + " seconds")
        except Exception as e:
            print(f"Failed to refresh token: {e}")
            self.access_token = None

    def __get_user_id(self):
        try:
            url = f"{self.nodejs_server_url}/userinfo"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            if self.debug:
                print(f"Requesting user info from Node.js server: {url}")
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            userinfo = response.json()
            if self.debug:
                # print("User info received:", userinfo)
                print("User info received")
            return userinfo.get("sub")
        except Exception as e:
            print(f"Failed to get user info: {e}")
            return None

    def __get_or_refresh(self):
        while self.run:
            try:
                if self.access_token is None:
                    self.__get_token()

                now = datetime.now()
                if self.expires_at < now:
                    if now < self.refresh_expires_at:
                        self.__refresh_token()
                    else:
                        self.__get_token()
            except Exception as e:
                self.access_token = None
                print(f"Error during token management: {e}")

            sleep(self.tick)

    def start(self):
        self.t = threading.Thread(target=self.__get_or_refresh, name="autodarts-tokenizer")
        self.t.start()
        return self.t

    def stop(self):
        self.run = False
        self.t.join()
        print(self.t.name + " EXIT")