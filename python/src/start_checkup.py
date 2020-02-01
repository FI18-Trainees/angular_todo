import os.path
import sys

from utils import Console, red, white, yellow, blue2

SHL = Console("Checkup")

if not os.path.exists(os.path.join("app", "public")):
    if "-unittest" in [x.strip().lower() for x in sys.argv]:  # start args
        SHL.warning(f"public folder is missing but ignored for unittest mode.")
    else:
        raise RuntimeError(f"{red}public folder is missing, use 'ng build --prod' and try again{white}")
    SHL.info(f"Start_checkup passed.")
