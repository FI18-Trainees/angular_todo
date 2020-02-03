import json

from flask import request, jsonify, make_response

from utils import Console, cfg
from .flask_app import app
from .authentication import token_auth, basic_auth
from .user_manager import user_manager
from .flask_limiter import limiter

SHL = Console("Routes")


@app.route("/login")
@basic_auth.login_required
@limiter.limit("20 per hour")
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


@app.route("/login/2fa")
@basic_auth.login_required
@limiter.limit("20 per hour")
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
        reset_token = bool(request_data.get("reset_token", False))
        access_token = user_manager.get_token() if reset_token else user_manager.gen_new_token()
        if user_manager.check_2fa(totp_token=token_2fa):
            data = {
                "login_status": "access_token generated",
                "login_status_code": 0,
                "access_token": access_token
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


@app.route("/login/rename", methods=["POST"])
@token_auth.login_required
@limiter.limit("20 per hour")
def login_rename():
    try:
        request_data = json.loads(request.data.decode('utf-8'))
    except json.JSONDecodeError:
        return make_response("invalid json", 400)
    new_name = request_data.get("new_name", None)
    if str(new_name).strip().lower() in ["null", "none", ""]:
        data = {
            "status": "failed",
            "message": "invalid name"
        }
        return make_response(jsonify(data), 400)
    new_name = str(new_name).strip()
    if len(new_name) not in range(1, 50):
        data = {
            "status": "failed",
            "message": "invalid name"
        }
        return make_response(jsonify(data), 400)
    if user_manager.rename(new=new_name):
        return jsonify(
            {
                "status": "success",
                "message": f"new name {new_name}"
            }
        )
    data = {
        "status": "failed",
        "message": "failed saving new name"
    }
    return make_response(jsonify(data), 500)


@app.route("/login/reset/password", methods=["POST"])
@token_auth.login_required
@limiter.limit("20 per hour")
def login_reset_password():
    try:
        request_data = json.loads(request.data.decode('utf-8'))
    except json.JSONDecodeError:
        return make_response("invalid json", 400)
    new_password = request_data.get("new_password", None)
    if str(new_password).strip().lower() in ["null", "none", ""]:
        data = {
            "status": "failed",
            "message": "invalid password"
        }
        return make_response(jsonify(data), 400)
    if user_manager.set_password(new=str(new_password)):
        return jsonify(
            {
                "status": "success",
            }
        )
    data = {
        "status": "failed",
        "message": "failed saving new password"
    }
    return make_response(jsonify(data), 500)


@app.route("/login/reset/token", methods=["POST"])
@token_auth.login_required
@limiter.limit("20 per hour")
def login_reset_token():
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
        "access_token": user_manager.gen_new_token()
    }
    return jsonify(data)


@app.route("/login/2fa/new", methods=["POST"])
@token_auth.login_required
@limiter.limit("20 per hour")
def login_2fa_new():
    data = {
        "status": "success",
        "message": "temp_2fa_token generated.",
        "link": user_manager.get_new_2fa_token()
    }
    return jsonify(data)


@app.route("/login/2fa/validate", methods=["POST"])
@token_auth.login_required
@limiter.limit("20 per hour")
def login_2fa_validate():
    try:
        request_data = json.loads(request.data.decode('utf-8'))
    except json.JSONDecodeError:
        return make_response("invalid json", 400)
    totp_token = request_data.get("totp_token", None)
    if str(totp_token).strip().lower() in ["null", "none", ""]:
        data = {
            "status": "failed",
            "message": "invalid totp_token"
        }
        return make_response(jsonify(data), 400)
    if user_manager.check_2fa_temp_token(totp_token=str(totp_token)):
        if user_manager.set_2fa_temp_token():
            data = {
                "status": "success",
                "message": "2fa enabled"
            }
            return jsonify(data)
        data = {
            "status": "failed",
            "message": "could not enable 2fa"
        }
        return make_response(jsonify(data), 500)
    data = {
        "status": "failed",
        "message": "invalid totp_token"
    }
    return make_response(jsonify(data), 400)


@app.route("/login/2fa/link")
@token_auth.login_required
def login_2fa_link():
    link = user_manager.get_2fa_link()
    data = {
        "status": "success" if link else "failed",
        "message": link if link else "2fa not enabled"
    }
    return make_response(jsonify(data), 200 if link else 412)


SHL.info(f"Registered login routes.")
