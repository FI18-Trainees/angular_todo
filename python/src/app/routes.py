import json
import os

from .flask_app import app
from flask import request, jsonify, make_response, send_from_directory

from utils import Console, cfg
from .authentication import token_auth
from .flask_limiter import limiter

SHL = Console("Routes")


@app.route("/")
@limiter.exempt
def index():
    return "OK"


@app.route("/401")
@limiter.exempt
def unauthorized_access():
    return "401"


@app.route("/secret")
@token_auth.login_required
def secret():
    return "secret"


@app.route('/public/<path:path>')
@limiter.exempt
def send_assets(path):
    return send_from_directory(os.path.join("public"), path)


SHL.info(f"Registered static routes.")
