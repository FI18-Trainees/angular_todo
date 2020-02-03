import json

from flask import make_response, jsonify, request

from .authentication import token_auth
from .flask_app import app
from utils import Console
from .obj import Todo
from .obj.errors import CreationError

SHL = Console("Routes")

dummy_todo_list = []


@app.route("/api/todo", methods=["GET", "POST"])
@token_auth.login_required
def api_todo():
    if request.method == "GET":
        SHL.info(f"Returning Todo list", f"GET /api/todo")
        return jsonify([x.to_json() for x in dummy_todo_list])
    if request.method == "POST":
        SHL.info(f"Creating Todo", f"POST /api/todo")
        try:
            request_data = json.loads(request.data.decode('utf-8'))
        except json.JSONDecodeError:
            return make_response("invalid json", 400)
        try:
            todo = Todo(**request_data)
        except CreationError:
            return make_response(jsonify({
                "status": "failed"
            }), 400)
        else:
            dummy_todo_list.append(todo)
            return jsonify({
                "status": "success"
            })
    return make_response("invalid method", 405)


SHL.info(f"Registered api routes.")