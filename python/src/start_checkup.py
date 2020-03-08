import os.path
import sys

from utils import Console, red, white

SHL = Console("Checkup")

if not os.path.exists(os.path.join("app", "public")):
    if "-unittest" in [x.strip().lower() for x in sys.argv]:  # start args
        SHL.warning(f"public folder is missing but ignored for unittest mode.")
        SHL.info(f"Creating dummy index.html for unittests.")
        os.mkdir(os.path.join("app", "public"))
        with open(os.path.join("app", "public", "index.html"), "w") as fh:
            fh.write("<body>ok<body/>")
    else:
        raise RuntimeError(f"{red}public folder is missing, use 'ng build --prod' and try again{white}")

SHL.info(f"Start_checkup passed.")
