import os
from datetime import datetime

from flask import send_from_directory, make_response, jsonify

from utils import Console
from app.flask_app import app
from app.authentication import token_auth
from app.flask_limiter import limiter
from app.db_connector import db_interface
from app.obj import DatabaseError, SQLTodoList

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
