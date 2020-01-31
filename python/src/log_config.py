import sys
import logging

from utils import Console, white, blue2

SHL = Console("Startup")

if "-log" in [x.strip().lower() for x in sys.argv]:
    SHL.output(f"{blue2}Setting loggers to info level.{white}")
else:
    SHL.output(f"{blue2}Setting loggers to error level.{white}")
    logging.getLogger('app').setLevel(logging.ERROR)
    logging.getLogger('app.flask_app').setLevel(logging.ERROR)
    logging.getLogger('flask').setLevel(logging.ERROR)
    logging.getLogger('flask.app').setLevel(logging.ERROR)
