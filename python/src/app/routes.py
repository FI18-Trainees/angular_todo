from .flask_app import app
from flask_limiter import Limiter
from flask import request

from utils import Console, white, blue2, cfg
from .authentication import auth

SHL = Console("Routes")


def determine_ip():
    if request.headers.get("X-Forwarded-For", request.remote_addr) == cfg.get("own_ip"):
        return request.headers.get("X-Auth-For", request.headers.get("X-Forwarded-For", request.remote_addr))
    return request.headers.get("X-Forwarded-For", request.remote_addr)


limiter = Limiter(
    app,
    key_func=lambda: determine_ip,
    default_limits=["10 per day", "5 per hour"],
)


@app.route("/")
def index():
    return "OK"


@app.route("/401")
def unauthorized_access():
    return "401"


@app.route("/secret")
@auth.login_required
def secret():
    return "secret"


# TODO: use this to login: either receive session token or temp token + request for 2fa
def login():
    pass


SHL.info(f"Registered routes.")
