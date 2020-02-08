import dateutil.parser

from utils import Console
from .errors import CreationError
from .sql_types import SQLTodoList

SHL = Console("TodoList")


class TodoList:
    def __init__(self, to_parse):
        if isinstance(to_parse, dict):
            # mandatory
            try:
                self.name = to_parse["name"]
                if self.name.strip().lower() in ["none", "null", ""]:
                    SHL.error(f"Failed creating TodoList. Invalid mandatory keys provided.")
                    raise CreationError(raw=to_parse)
            except KeyError:
                SHL.error(f"Failed creating TodoList. Mandatory key missing.")
                raise CreationError(raw=to_parse)
            except ValueError:
                SHL.error(f"Failed creating TodoList. Invalid mandatory keys provided.")
                raise CreationError(raw=to_parse)

            # optional
            try:
                self.list_id = int(to_parse.get("list_id"))
            except ValueError:
                self.list_id = None
            except TypeError:
                self.list_id = None
            if to_parse.get("created_at"):
                self.created_at = dateutil.parser.isoparse(to_parse.get("created_at"))
            else:
                self.created_at = None
            self.hex_color = to_parse.get("hex_color")
            self.description = to_parse.get("description")
        elif isinstance(to_parse,  SQLTodoList):
            # mandatory
            try:
                self.list_id = int(to_parse.list_id)
                self.name = to_parse.name
            except AttributeError:
                SHL.error(f"Failed creating TodoList. Mandatory key missing.")
                raise CreationError(raw=to_parse)
            except ValueError:
                SHL.error(f"Failed creating TodoList. Invalid mandatory keys provided.")
                raise CreationError(raw=to_parse)

            # optional
            if to_parse.created_at:
                self.created_at = dateutil.parser.isoparse(str(to_parse.created_at))
            else:
                self.created_at = None
            self.hex_color = to_parse.hex_color
            self.description = to_parse.description

        else:
            SHL.error(f"Failed creating TodoList. Invalid internal input type.")
            SHL.error(f"Type provided: {type(to_parse)}")
            raise CreationError(raw=to_parse)

    def to_json(self) -> dict:
        return {
            "list_id": int(self.list_id),
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "hex_color": self.hex_color,
        }

    def to_sql_obj(self) -> SQLTodoList:
        x = SQLTodoList(
            name=self.name,
            description=self.description,
            created_at=self.created_at,
            hex_color=self.hex_color
        )
        if self.list_id:
            x.list_id = self.list_id
        return x
