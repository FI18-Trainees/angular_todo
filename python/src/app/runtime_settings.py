import sys

from utils import Console, white, cfg, red

SHL = Console("SettingsInit")

start_args = [x.strip().lower() for x in sys.argv]


login_disabled = cfg.get("logindisabled", False)  # default from cfg
if "-disablelogin" in start_args:  # overwrite by parameter
    login_disabled = True

if login_disabled:
    SHL.info(f"Disabled authentication.")

debug_mode = cfg.get("debug_enabled", False)  # default from cfg
if "-debug" in start_args:  # overwrite by parameter
    debug_mode = True

if debug_mode:
    SHL.info(f"Enabled debug_mode.")

unittest_mode = False
if "-unittest" in start_args:
    SHL.info(f"Enabled unittest mode.")
    unittest_mode = True
    debug_mode = False
    cfg.load_unittest_config()

production_mode = False
if "-prod" in start_args:
    SHL.info(f"Enabled production mode.")
    production_mode = True


if unittest_mode and production_mode:
    raise RuntimeError(f"{red}Unittest and production mode cannot be enabled simultaneously.{white}")
