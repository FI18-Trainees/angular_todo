import json

from flask import make_response, jsonify, request
from sqlalchemy.orm.exc import NoResultFound

from utils import Console
from app.authentication import token_auth
from app.flask_app import app
from app.obj import Todo, TodoList, CreationError, DatabaseError
from app.db_connector import db_interface

SHL = Console("Routes")


@app.route("/api/todo", methods=["GET", "POST", "DELETE", "PATCH"])
@token_auth.login_required
def api_todo():
    if request.method == "GET":
        if request.args.get("list_id"):
            SHL.info(f"Returning Todo by list_id", f"GET /api/todo")
            try:
                list_id = int(request.args.get("list_id"))
            except ValueError:
                SHL.warning(f"Invalid list_id provided", f"GET /api/todo")
                return make_response(jsonify({
                    "status": "failed",
                    "message": "invalid list_id"
                }), 400)
            except TypeError:
                SHL.warning(f"Invalid list_id provided", f"GET /api/todo")
                return make_response(jsonify({
                    "status": "failed",
                    "message": "invalid list_id"
                }), 400)
            try:
                received_entries = [x for x in db_interface.todo_select_by_list_id(list_id=list_id)]
            except DatabaseError:
                return make_response(jsonify({
                    "status": "failed",
                    "message": "database error"
                }), 500)
            except NoResultFound:
                received_entries = None
            if received_entries:
                SHL.info(f"Returning {len(received_entries)} entries.", f"GET /api/todo")
                return jsonify({
                    "status": "success",
                    "message": f"{len(received_entries)} entry found.",
                    "data": [x.to_json() for x in received_entries]
                })
            else:
                SHL.info(f"No entries found.", f"GET /api/todo")
                return jsonify({
                    "status": "failed",
                    "message": "no entries found.",
                    "data": None
                })
        elif request.args.get("item_id"):
            SHL.info(f"Returning Todo by item_id", f"GET /api/todo")
            try:
                item_id = int(request.args.get("item_id"))
            except ValueError:
                SHL.warning(f"Invalid item_id provided", f"GET /api/todo")
                return make_response(jsonify({
                    "status": "failed",
                    "message": "invalid item_id"
                }), 400)
            except TypeError:
                SHL.warning(f"Invalid item_id provided", f"GET /api/todo")
                return make_response(jsonify({
                    "status": "failed",
                    "message": "invalid item_id"
                }), 400)
            try:
                received_entries = db_interface.todo_select_by_item_id(item_id=item_id)
            except DatabaseError:
                return make_response(jsonify({
                    "status": "failed",
                    "message": "database error"
                }), 500)
            except NoResultFound:
                received_entries = None
            if received_entries:
                SHL.info(f"Returning 1 entries.", f"GET /api/todo")
                return jsonify({
                    "status": "success",
                    "message": f"{len(received_entries)} entry found.",
                    "data": received_entries.to_json()
                })
            else:
                SHL.info(f"No entries found.", f"GET /api/todo")
                return jsonify({
                    "status": "failed",
                    "message": "no entries found.",
                    "data": None
                })
        elif request.args.get("finished"):
            SHL.info(f"Returning Todo by finished", f"GET /api/todo")
            try:
                finished = int(request.args.get("finished"))
            except ValueError:
                SHL.warning(f"Invalid finished provided", f"GET /api/todo")
                return make_response(jsonify({
                    "status": "failed",
                    "message": "invalid finished"
                }), 400)
            except TypeError:
                SHL.warning(f"Invalid finished provided", f"GET /api/todo")
                return make_response(jsonify({
                    "status": "failed",
                    "message": "invalid finished"
                }), 400)
            try:
                received_entries = [x for x in db_interface.todo_select_by_finished(finished=finished)]
            except DatabaseError:
                return make_response(jsonify({
                    "status": "failed",
                    "message": "database error"
                }), 500)
            except NoResultFound:
                received_entries = None
            if received_entries:
                SHL.info(f"Returning {len(received_entries)} entries.", f"GET /api/todo")
                return jsonify({
                    "status": "success",
                    "message": f"{len(received_entries)} entry found.",
                    "data": [x.to_json() for x in received_entries]
                })
            else:
                SHL.info(f"No entries found.", f"GET /api/todo")
                return jsonify({
                    "status": "failed",
                    "message": "no entries found.",
                    "data": None
                })
        else:
            SHL.info(f"Returning Todo", f"GET /api/todo")
            try:
                received_entries = [x for x in db_interface.todo_select_all()]
            except DatabaseError:
                return make_response(jsonify({
                    "status": "failed",
                    "message": "database error"
                }), 500)
            if received_entries:
                SHL.info(f"Returning {len(received_entries)} entries.", f"GET /api/todo")
                return jsonify({
                    "status": "success",
                    "message": f"{len(received_entries)} entries found.",
                    "data": [x.to_json() for x in received_entries]
                })
            else:
                SHL.info(f"No entries found.", f"GET /api/todo")
                return jsonify({
                    "status": "failed",
                    "message": "no entries found.",
                    "data": []
                })
    if request.method == "POST":
        SHL.info(f"Creating Todo", f"POST /api/todo")
        try:
            request_data = json.loads(request.data.decode('utf-8'))
        except json.JSONDecodeError:
            return make_response(jsonify({
                "status": "failed",
                "message": "invalid json"
            }), 400)
        try:
            request_data.pop("item_id", None)
            db_interface.todo_insert_or_update(obj=Todo(to_parse=request_data).to_sql_obj())
        except CreationError as e:
            return make_response(jsonify({
                "status": "failed",
                "message": e.get_error_message()
            }), 400)
        except DatabaseError:
            return make_response(jsonify({
                "status": "failed",
                "message": "database error"
            }), 500)
        else:
            return jsonify({
                "status": "success",
                "message": "todo created"
            })
    if request.method == "DELETE":
        return make_response("OK", 501)
    if request.method == "PATCH":
        return make_response("OK", 501)

    return make_response("invalid method", 405)


@app.route("/api/todolist", methods=["GET", "POST", "DELETE", "PATCH"])
@token_auth.login_required
def api_todo_list():
    if request.method == "GET":
        if request.args.get("list_id"):
            SHL.info(f"Returning TodoList by list_id", f"GET /api/todolist")
            try:
                list_id = int(request.args.get("list_id"))
            except ValueError:
                SHL.warning(f"Invalid list_id provided", f"GET /api/todolist")
                return make_response(jsonify({
                    "status": "failed",
                    "message": "invalid list_id"
                }), 400)
            except TypeError:
                SHL.warning(f"Invalid list_id provided", f"GET /api/todolist")
                return make_response(jsonify({
                    "status": "failed",
                    "message": "invalid list_id"
                }), 400)
            try:
                received_entries = db_interface.todo_list_select_by_list_id(list_id=list_id)
            except DatabaseError:
                return make_response(jsonify({
                    "status": "failed",
                    "message": "database error"
                }), 500)
            except NoResultFound:
                received_entries = None
            if received_entries:
                SHL.info(f"Returning 1 entries.", f"GET /api/todolist")
                return jsonify({
                    "status": "success",
                    "message": "1 entry found.",
                    "data": received_entries.to_json()
                })
            else:
                SHL.info(f"No entries found.", f"GET /api/todolist")
                return jsonify({
                    "status": "failed",
                    "message": "no entries found.",
                    "data": None
                })
        SHL.info(f"Returning TodoList", f"GET /api/todolist")
        try:
            received_entries = [x for x in db_interface.todo_list_select_all()]
        except DatabaseError:
            return make_response(jsonify({
                "status": "failed",
                "message": "database error"
            }), 500)
        if received_entries:
            SHL.info(f"Returning {len(received_entries)} entries.", f"GET /api/todolist")
            return jsonify({
                "status": "success",
                "message": f"{len(received_entries)} entries found.",
                "data": [x.to_json() for x in received_entries]
            })
        else:
            SHL.info(f"No entries found.", f"GET /api/todolist")
            return jsonify({
                "status": "failed",
                "message": "no entries found.",
                "data": []
            })
    if request.method == "POST":
        SHL.info(f"Creating Todo", f"POST /api/todolist")
        try:
            request_data = json.loads(request.data.decode('utf-8'))
        except json.JSONDecodeError:
            return make_response(jsonify({
                "status": "failed",
                "message": "invalid json"
            }), 400)
        try:
            request_data.pop("list_id", None)
            request_data.pop("created_at", None)
            db_interface.todo_list_insert_or_update(obj=TodoList(to_parse=request_data).to_sql_obj())
        except CreationError as e:
            return make_response(jsonify({
                "status": "failed",
                "message": e.get_error_message()
            }), 400)
        except DatabaseError:
            return make_response(jsonify({
                "status": "failed",
                "message": "database error"
            }), 500)
        else:
            return jsonify({
                "status": "success",
                "message": "todolist created"
            })
    if request.method == "DELETE":
        return make_response("OK", 501)
    if request.method == "PATCH":
        return make_response("OK", 501)

    return make_response("invalid method", 405)


SHL.info(f"Registered api routes.")
