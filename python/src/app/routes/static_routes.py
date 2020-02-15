import os

from flask import send_from_directory, make_response

from utils import Console
from app.flask_app import app
from app.authentication import token_auth
from app.rate_limiter import limiter

SHL = Console("Routes")


@app.route("/")
@limiter.exempt
def index():
    return "OK"


@app.route("/401")
@limiter.exempt
def unauthorized_access():
    return make_response("401", 401)


@app.route("/secret")
@token_auth.login_required
def secret():
    return "secret"


@app.route('/public/<path:path>')
@limiter.exempt
def send_assets(path):
    return send_from_directory(os.path.join("public"), path)


SHL.info(f"Registered static routes.")
