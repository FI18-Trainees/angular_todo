import json

from .flask_app import app
from flask_limiter import Limiter
from flask import request, jsonify, make_response

from utils import Console, white, blue2, cfg
from .authentication import auth, basic_auth
from .user_manager import user_manager

SHL = Console("Routes")


def determine_ip():
    if request.headers.get("X-Forwarded-For", request.remote_addr) == cfg.get("own_ip"):
        return request.headers.get("X-Auth-For", request.headers.get("X-Forwarded-For", request.remote_addr))
    return request.headers.get("X-Forwarded-For", request.remote_addr)


limiter = Limiter(
    app,
    key_func=lambda: determine_ip,
    default_limits=["10000 per day", "50 per hour"],
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


@app.route("/login")
@basic_auth.login_required
def login():
    if user_manager.use_2fa:
        data = {
            "login_status": "2fa required",
            "login_status_code": 1,
            "temp_token": user_manager.get_temp_token()
        }
        return jsonify(data)
    data = {
        "login_status": "access_token generated",
        "login_status_code": 0,
        "access_token": user_manager.get_token()
    }
    return jsonify(data)


@app.route("/login2fa")
@basic_auth.login_required
def login_2fa():
    if not user_manager.use_2fa:
        data = {
            "login_status": "2fa not enabled",
            "login_status_code": 4
        }
        return make_response(jsonify(data), 412)
    temp_token = request.cookies.get("temp_token", None)
    if user_manager.check_temp_token(temp_token):
        try:
            request_data = json.loads(request.data.decode('utf-8'))
        except json.JSONDecodeError:
            return make_response("invalid json", 400)
        token_2fa = request_data.get("token_2fa", None)
        if user_manager.check_2fa(totp_token=token_2fa):
            data = {
                "login_status": "access_token generated",
                "login_status_code": 0,
                "access_token": user_manager.get_token()
            }
            return jsonify(data)
        data = {
            "login_status": "2fa invalid",
            "login_status_code": 3
        }
        return make_response(jsonify(data), 401)
    data = {
        "login_status": "invalid temp token",
        "login_status_code": 2
    }
    return make_response(jsonify(data), 401)


SHL.info(f"Registered routes.")
