import json

from .flask_app import app
from flask import request, jsonify, make_response

from utils import Console, cfg
from .authentication import token_auth
from .flask_limiter import limiter

SHL = Console("Routes")


@app.route("/")
def index():
    return "OK"


@app.route("/401")
def unauthorized_access():
    return "401"


@app.route("/secret")
@token_auth.login_required
def secret():
    return "secret"


SHL.info(f"Registered static routes.")
