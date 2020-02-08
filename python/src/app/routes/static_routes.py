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
    try:
        x = []
        for e in db_interface.todo_list_select_all():
            x.append(e.to_json())
        return jsonify(x)
    except DatabaseError:
        return "error"


@app.route("/1")
@limiter.exempt
def test():
    try:
        x = db_interface.todo_list_select_by_list_id(list_id=5)
        if x:
            return x.to_json()
        return "none"
    except DatabaseError:
        return "error"


@app.route("/2")
def test2():
    a = SQLTodoList(
        name="name1",
        description="dawdaw",
        hex_color="#454545",
        created_at=datetime.now()
    )
    try:
        x = db_interface.todo_list_insert(insert_obj=a)
        print(x)
        print(type(x))
        return "OK"
    except DatabaseError:
        return "error"


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
