import dateutil.parser

from utils import Console
from .errors import CreationError

SHL = Console("Todo")


class Todo:
    def __init__(self, **kwargs):
        # mandatory
        try:
            self.id = int(kwargs["id"])
            self.title = kwargs["title"]
            self.finished = bool(kwargs["finished"])
        except KeyError:
            SHL.error(f"Failed creating Todo. Mandatory key missing.")
            raise CreationError(raw=kwargs)
        except ValueError:
            SHL.error(f"Failed creating Todo. Invalid mandatory keys provided.")
            raise CreationError(raw=kwargs)

        # optional
        if kwargs.get("date"):
            self.due_date = dateutil.parser.isoparse(kwargs.get("date"))
        else:
            self.due_date = None
        self.address = kwargs.get("address")
        self.description = kwargs.get("description")
        try:
            self.priority = int(kwargs.get("priority", 0))
        except ValueError:
            self.priority = 0
        self.subtasks = kwargs.get("subtasks", [])
        if kwargs.get("reminder"):
            self.reminder = dateutil.parser.isoparse(kwargs.get("reminder"))
        else:
            self.reminder = None

    def to_json(self) -> dict:
        return {
            "id": int(self.id),
            "title": self.title,
            "finished": bool(self.finished),
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "address": self.address,
            "description": self.description,
            "priority": int(self.priority),
            "subtasks": self.subtasks,
            "reminder": self.reminder.isoformat() if self.reminder else None
        }
