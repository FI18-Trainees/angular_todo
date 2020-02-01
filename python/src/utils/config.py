import os.path
import json

from .shell import Console, blue2, white, yellow

BASE_PATH = "config" if os.path.isdir("config") else "config-default"

PATHS = ["main.json"]
SHL = Console("cfg", cls=True)


class __Config:
    def __init__(self, debug: bool = False):
        self.options = {}
        self.reload(debug=debug)

    def reload(self, debug: bool = False):
        SHL.info(f"Reloading config.")
        for path in PATHS:
            SHL.info(f"Reloading configfile {os.path.join(BASE_PATH, path)}")
            try:
                with open(os.path.join(BASE_PATH, path), 'r', encoding="utf-8") as c:
                    data = json.load(c)
            except FileNotFoundError:
                continue
            except json.JSONDecodeError:
                continue

            for key, value in data.items():
                self.options[key] = value
                if debug:
                    SHL.output(f"[{key}]: {value}")

    def get(self, key: str, default=None):
        return self.options.get(key, default)

    def load_unittest_config(self, debug: bool = False):
        SHL.info(f"Loading unittest configfile {os.path.join(BASE_PATH, 'unittest.json')}")
        try:
            with open(os.path.join(BASE_PATH, 'unittest.json'), 'r', encoding="utf-8") as c:
                data = json.load(c)
        except FileNotFoundError:
            SHL.warning(f"unittest configfile '{os.path.join(BASE_PATH, 'unittest.json')}' not found.")
            return
        except json.JSONDecodeError:
            SHL.warning(f"'{os.path.join(BASE_PATH, 'unittest.json')}' is not a valid json.")
            return

        for key, value in data.items():
            self.options[key] = value
            if debug:
                SHL.output(f"[{key}]: {value}")


cfg = __Config()
