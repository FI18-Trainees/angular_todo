import sys

import start_checkup
import log_config
from utils import Console, cfg, white, red
from app import app

SHL = Console("Startup")


def run():
    port = cfg.get("port", 5000)
    start_args = [x.strip().lower() for x in sys.argv]

    if "-port" in start_args:
        try:
            port = int(sys.argv[sys.argv.index("-port") + 1])
        except IndexError:
            pass
        except ValueError:
            raise RuntimeError(f'{red}Invalid port "{sys.argv[sys.argv.index("-port") + 1]}"{white}')

    if "--cfg-debug" in start_args:
        cfg.reload(debug=True)

    SHL.output("Starting up.")
    SHL.info(f"Using port: {port}")

    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    run()
