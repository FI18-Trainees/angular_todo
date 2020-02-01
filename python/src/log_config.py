import sys
import logging

from utils import Console, white, blue2

SHL = Console("Startup")

if "-log" in [x.strip().lower() for x in sys.argv]:
    SHL.info(f"Setting loggers to info level.")
else:
    SHL.info(f"Setting loggers to error level.")
    logging.getLogger('app').setLevel(logging.ERROR)
    logging.getLogger('app.flask_app').setLevel(logging.ERROR)
    logging.getLogger('flask').setLevel(logging.ERROR)
    logging.getLogger('flask.app').setLevel(logging.ERROR)
