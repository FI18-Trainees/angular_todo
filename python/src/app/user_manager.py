from datetime import datetime, timedelta
import os.path
import json
import uuid
from typing import Optional

from werkzeug.security import generate_password_hash, check_password_hash
import pyotp

from utils import Console, red, white, cfg
from .runtime_settings import production_mode

SHL = Console("UserManager")

SHL.info(f"Initializing UserManager.")

BASE_PATH = os.path.dirname(__file__)
login_file = "login.json" if os.path.isfile(os.path.join(BASE_PATH, "login.json")) else "login-default.json"
LOGIN_INFO = os.path.join(BASE_PATH, login_file)
SHL.info(f"Login info in file {LOGIN_INFO}")


class __UserManager:
    def __init__(self):
        SHL.info(f"Loading login info.")
        try:
            with open(LOGIN_INFO, 'r', encoding="utf-8") as fh:
                data = json.load(fh)
        except FileNotFoundError:
            if production_mode:
                raise RuntimeError(f"{red}login.json not found. "
                                   f"Authentication of some sort is required in production mode.{white}")
            SHL.error("Login info not found. Using dummy user.")
            return
        except json.JSONDecodeError:
            if production_mode:
                raise RuntimeError(f"{red}login.json is not valid. "
                                   f"Authentication of some sort is required in production mode.{white}")
            SHL.error("Login info not found. Using dummy user.")
            return

        SHL.info(f"Setting user data.")
        self.username = str(data.get("user", "dummy"))
        self.password = str(data.get("pass", "dummy"))
        self.token = str(data.get("token", None))
        self.expire_at = datetime.utcnow() + timedelta(seconds=cfg.get("token_expire_seconds", 86400))
        self.use_2fa = bool(data.get("use2fa", False))
        self.token_2fa = data.get("token_2fa", None)
        self.token_2fa_temp = None
        self.temp_token = None
        self.temp_token_expire_at = datetime.utcnow() + timedelta(seconds=30)

        if self.use_2fa and self.token_2fa:
            self.pyotp_session = pyotp.TOTP(self.token_2fa)

    def rename(self, new: str) -> bool:
        SHL.info(f"Setting new username '{new}'")
        self.username = new
        self.__save_newest_data()
        return True

    def login(self, username: str, password: str) -> bool:
        SHL.info(f"Check credentials for '{username}' and password length {len(password)}.")
        return username == self.username and check_password_hash(self.password, password)

    def get_temp_token(self) -> str:
        if not self.temp_token:
            self.temp_token = str(uuid.uuid4())
            self.temp_token_expire_at = datetime.utcnow() + timedelta(seconds=30)
        if self.temp_token_expire_at < datetime.utcnow():
            self.temp_token = str(uuid.uuid4())
            self.temp_token_expire_at = datetime.utcnow() + timedelta(seconds=30)
        return self.temp_token

    def check_temp_token(self, token: str) -> bool:
        if not self.temp_token:
            return False
        if self.temp_token_expire_at < datetime.utcnow():
            return False
        return self.temp_token == token

    def set_password(self, new: str) -> bool:
        self.password = generate_password_hash(new)
        self.__save_newest_data()
        return True

    def get_token(self) -> str:
        if not self.token:
            self.token = str(uuid.uuid4())
            self.expire_at = datetime.utcnow() + timedelta(seconds=cfg.get("token_expire_seconds", 86400))
            self.__save_newest_data()
        if self.expire_at < datetime.utcnow():
            self.token = str(uuid.uuid4())
            self.expire_at = datetime.utcnow() + timedelta(seconds=cfg.get("token_expire_seconds", 86400))
            self.__save_newest_data()
        return self.token

    def gen_new_token(self) -> str:
        self.token = str(uuid.uuid4())
        self.expire_at = datetime.utcnow() + timedelta(seconds=cfg.get("token_expire_seconds", 86400))
        self.__save_newest_data()
        return self.token

    def check_token(self, token: str) -> bool:
        if not self.token:
            return False
        if self.expire_at < datetime.utcnow():
            return False
        return self.token == token

    def get_new_2fa_token(self) -> str:
        self.token_2fa_temp = pyotp.random_base32()
        return pyotp.TOTP(self.token_2fa_temp).provisioning_uri(f"{self.username}", issuer_name="TODO")

    def check_2fa_temp_token(self, totp_token: str) -> bool:
        if self.token_2fa_temp:
            return pyotp.utils.strings_equal(pyotp.TOTP(self.token_2fa_temp).now(), totp_token)
        else:
            return False

    def set_2fa_temp_token(self) -> bool:
        if self.token_2fa_temp:
            self.pyotp_session = pyotp.TOTP(self.token_2fa_temp)
            self.token_2fa = self.token_2fa_temp
            self.use_2fa = True
            self.token = None
            self.token_2fa_temp = None
            self.__save_newest_data()
            return True
        else:
            return False

    def get_2fa_link(self) -> Optional[str]:
        if isinstance(self.pyotp_session, pyotp.totp.TOTP):
            return self.pyotp_session.provisioning_uri(f"{self.username}", issuer_name="TODO")
        return None

    def check_2fa(self, totp_token: str) -> bool:
        if isinstance(self.pyotp_session, pyotp.totp.TOTP):
            return pyotp.utils.strings_equal(self.pyotp_session.now(), totp_token)
        return False

    def __save_newest_data(self):
        SHL.info(f"Saving newest login info to file.")
        data = {
          "user": self.username,
          "pass": self.password,
          "token": self.token,
          "use2fa": self.use_2fa,
          "token_2fa": self.token_2fa
        }
        try:
            with open(os.path.join(BASE_PATH, "login.json"), 'w', encoding="utf-8") as outfile:
                json.dump(data, outfile)
        except FileNotFoundError:
            SHL.error(f"Could not write newest login info to json.")
            return
        except json.JSONDecodeError:
            SHL.error(f"Could not write newest login info to json.")
            return


user_manager = __UserManager()
