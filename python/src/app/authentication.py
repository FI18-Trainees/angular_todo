from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth
from flask import redirect, request

from .runtime_settings import login_disabled

auth = HTTPTokenAuth()
basic_auth = HTTPBasicAuth()


@auth.error_handler
def auth_error():
    if str(request.script_root + request.path).strip() != "/":
        return redirect(f"/401?redirect={request.script_root + request.path}")
    return redirect(f"/401")


@auth.verify_token
def verify_token(token):
    return False
