from datetime import datetime, timedelta
from time import sleep
from keycloak import KeycloakOpenID
import threading


class AutodartsKeycloakClient:
    token_lifetime_fraction = 0.9
    tick: int = 3
    run: bool = True
    username: str = None
    password: str = None
    debug: bool = False
    kc: KeycloakOpenID = None
    access_token: str = None
    refresh_token: str = None
    user_id: str = None
    expires_at: datetime = None
    refresh_expires_at: datetime = None
    t: threading.Thread = None


    def __init__(self, *, username: str, password: str, client_id: str, client_secret: str = None, debug: bool = False):
        self.kc = KeycloakOpenID(
            server_url="https://login.autodarts.io",
            client_id=client_id,
            client_secret_key=client_secret,
            realm_name="autodarts",
            verify=True
        )
        self.username = username
        self.password = password
        self.debug = debug

        self.__get_token()
        self.user_id = self.kc.userinfo(self.access_token)['sub']

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
        self.__set_token(self.kc.token(self.username, self.password))
        if self.debug:
            print("Getting token", self.expires_at, self.refresh_expires_at)

    def __refresh_token(self):
        self.__set_token(self.kc.refresh_token(self.refresh_token))
        if self.debug:
            print("Refreshing token", self.expires_at, self.refresh_expires_at)

    def __get_or_refresh(self):
          while self.run:
            # if self.debug:
                # print("Check token ..")

            if self.access_token is None:
                self.__get_token()

            now = datetime.now()
            if self.expires_at < now:
                if now < self.refresh_expires_at:
                    self.__refresh_token()
                else:
                    self.__get_token()

            sleep(self.tick)
                

    def start(self):
        self.t = threading.Thread(target=self.__get_or_refresh, name="autodarts-tokenizer")
        self.t.start()
        return self.t
    
    def stop(self):
        self.run = False
        self.t.join()
        print(self.t.name + " EXIT")



