import sys

from utils import Console, white, cfg, blue2

SHL = Console("SettingsInit")


start_args = [x.strip().lower() for x in sys.argv]
login_disabled = cfg.get("logindisabled", False)  # default from cfg
if "-disablelogin" in start_args:  # overwrite by parameter
    login_disabled = True

if login_disabled:
    SHL.info(f"Disabled authentication.")

debug_mode = cfg.get("debug_enabled", False)
if "-debug" in start_args:
    debug_mode = True

if debug_mode:
    SHL.info(f"Enabled debug_mode.")

if "-unittest" in start_args:
    SHL.info(f"Enabled unittest mode.")
    login_disabled = True
    debug_mode = False
    cfg.load_unittest_config()
