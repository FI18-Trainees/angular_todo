import dateutil.parser

from utils import Console
from .errors import CreationError
from .sql_types import SQLTodo

SHL = Console("Todo")


class Todo:
    def __init__(self, to_parse):
        if isinstance(to_parse, dict):
            # mandatory
            try:
                self.title = to_parse["title"]
                self.finished = bool(to_parse["finished"])
                self.list_id = int(to_parse["list_id"])
                if self.title.strip().lower() in ["none", "null", ""]:
                    SHL.error(f"Failed creating Todo. Invalid mandatory keys provided.")
                    raise CreationError(raw=to_parse)
            except KeyError:
                SHL.error(f"Failed creating Todo. Mandatory key missing.")
                raise CreationError(raw=to_parse)
            except ValueError:
                SHL.error(f"Failed creating Todo. Invalid mandatory keys provided.")
                raise CreationError(raw=to_parse)

            # optional
            try:
                self.item_id = int(to_parse.get("item_id"))
            except ValueError:
                self.item_id = None
            except TypeError:
                self.item_id = None
            if to_parse.get("due_date"):
                self.due_date = dateutil.parser.isoparse(to_parse.get("due_date"))
            else:
                self.due_date = None
            self.address = to_parse.get("address")
            self.description = to_parse.get("description")
            try:
                self.priority = int(to_parse.get("priority", 0))
            except ValueError:
                self.priority = 0
            self.subtasks = to_parse.get("subtasks", [])
            if to_parse.get("reminder"):
                self.reminder = dateutil.parser.isoparse(to_parse.get("reminder"))
            else:
                self.reminder = None

        elif isinstance(to_parse, SQLTodo):
            # mandatory
            try:
                self.item_id = int(to_parse.item_id)
                self.title = to_parse.title
                self.finished = bool(to_parse.finished)
                self.list_id = int(to_parse.list_id)
            except KeyError:
                SHL.error(f"Failed creating Todo. Mandatory key missing.")
                raise CreationError(raw=to_parse)
            except ValueError:
                SHL.error(f"Failed creating Todo. Invalid mandatory keys provided.")
                raise CreationError(raw=to_parse)

            # optional
            if to_parse.due_date:
                self.due_date = dateutil.parser.isoparse(to_parse.due_date)
            else:
                self.due_date = None
            self.address = to_parse.address
            self.description = to_parse.description
            try:
                self.priority = int(to_parse.priority)
            except ValueError:
                self.priority = 0
            self.subtasks = to_parse.subtasks
            if to_parse.reminder:
                self.reminder = dateutil.parser.isoparse(to_parse.reminder)
            else:
                self.reminder = None

        else:
            SHL.error(f"Failed creating Todo. Invalid internal input type.")
            SHL.error(f"Type provided: {type(to_parse)}")
            raise CreationError(raw=to_parse)

    def to_json(self) -> dict:
        return {
            "item_id": int(self.item_id),
            "title": self.title,
            "finished": bool(self.finished),
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "address": self.address,
            "description": self.description,
            "priority": int(self.priority),
            "subtasks": self.subtasks,
            "reminder": self.reminder.isoformat() if self.reminder else None
        }

    def to_sql_obj(self) -> SQLTodo:
        x = SQLTodo(
            title=self.title,
            finished=int(self.finished),
            due_date=self.due_date,
            address=self.address,
            description=self.description,
            priority=int(self.priority),
            subtasks=self.subtasks,
            reminder=self.reminder
        )
        if self.item_id:
            x.item_id = self.item_id
        return x
