from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth
from flask import redirect, request

from .runtime_settings import login_disabled
from .user_manager import user_manager

token_auth = HTTPTokenAuth()
basic_auth = HTTPBasicAuth()


@token_auth.error_handler
def auth_error():
    if str(request.script_root + request.path).strip() != "/":
        return redirect(f"/401?redirect={request.script_root + request.path}")
    return redirect(f"/401")


@token_auth.verify_token
def verify_token(token):
    if login_disabled:
        return True
    token = request.cookies.get("access_token", request.headers.get("Authorization", None))
    if str(token).strip().lower() in ["null", "none", ""]:
        return False
    return user_manager.check_token(token=token)


@basic_auth.verify_password
def verify_password(username, password):
    if login_disabled:
        return True
    if str(username).strip().lower() in ["null", "none", ""]:
        return False
    if str(password).strip().lower() in ["null", "none", ""]:
        return False
    return user_manager.login(username=username, password=password)
