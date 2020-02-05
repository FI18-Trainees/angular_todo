from flask import request
from flask_limiter import Limiter

from utils import cfg, Console
from .flask_app import app
from .runtime_settings import unittest_mode

SHL = Console("RateLimiter")


def determine_ip():
    if request.headers.get("X-Forwarded-For", request.remote_addr) == cfg.get("own_ip"):
        return request.headers.get("X-Auth-For", request.headers.get("X-Forwarded-For", request.remote_addr))
    return request.headers.get("X-Forwarded-For", request.remote_addr)


defaults = ["10000000 per day", "500000 per hour"] if unittest_mode else ["10000 per day", "500 per hour"]

limiter = Limiter(
    app,
    key_func=lambda: determine_ip,
    default_limits=["10000 per day", "500 per hour"],
)

SHL.info(f"Registered flask limiter.")
