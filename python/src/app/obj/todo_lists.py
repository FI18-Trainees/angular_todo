import dateutil.parser
from datetime import datetime

from utils import Console
from .errors import CreationError, DataMissingError, InvalidValueError, InvalidInputTypeError
from .sql_types import SQLTodoList

SHL = Console("TodoList")


def return_raw(raw):
    return raw


def get_value_and_parse(raw, key_attribute: str, parse_method, optional: bool = True, default=None):
    if isinstance(raw, dict):
        try:
            value = raw[key_attribute]
        except KeyError:
            value = default
            if not optional:
                SHL.error(f"Failed creating TodoList. Mandatory key '{key_attribute}' missing.")
                raise DataMissingError(missing_key=key_attribute)
    else:
        try:
            value = raw.__getattribute__(key_attribute)
        except AttributeError:
            value = default
            if not optional:
                SHL.error(f"Failed creating TodoList. Mandatory key '{key_attribute}' missing.")
                raise DataMissingError(missing_key=key_attribute)

    if value is not None:
        try:
            value = parse_method(value)
            if parse_method == str:
                if value.strip().lower() in ["none", "null", ""]:
                    SHL.error(f"Failed creating TodoList. Invalid key '{key_attribute}' provided.")
                    raise InvalidValueError(name_of_invalid=key_attribute)
            return value
        except ValueError:
            SHL.error(f"Failed creating TodoList. Invalid key '{key_attribute}' provided.")
            raise InvalidValueError(name_of_invalid=key_attribute)
        except TypeError:
            SHL.error(f"Failed creating TodoList. Invalid key '{key_attribute}' provided.")
            raise InvalidValueError(name_of_invalid=key_attribute)
    else:
        if isinstance(raw, SQLTodoList):
            return None
        if optional:
            return default
        else:
            SHL.error(f"Failed creating TodoList. Mandatory key '{key_attribute}' missing.")
            raise DataMissingError(missing_key=key_attribute)


class TodoList:
    def __init__(self, to_parse):
        if any([isinstance(to_parse, x) for x in [dict, SQLTodoList]]):  # check for valid inputs
            # mandatory
            self.name = get_value_and_parse(to_parse, "name", parse_method=str, optional=False)

            # optional
            self.hex_color = get_value_and_parse(to_parse, "hex_color", parse_method=str, default="#FFFFFF")
            self.description = get_value_and_parse(to_parse, "description", parse_method=str)

            if isinstance(to_parse, dict):
                self.created_at = datetime.now()
                self.list_id = get_value_and_parse(to_parse, "list_id", parse_method=int)
            else:
                self.created_at = get_value_and_parse(to_parse, "created_at", parse_method=return_raw)
                self.list_id = get_value_and_parse(to_parse, "list_id", parse_method=int, optional=False)

        else:
            SHL.error(f"Failed creating TodoList. Invalid internal input type.")
            SHL.error(f"Type provided: {type(to_parse)}")
            raise InvalidInputTypeError(type_provided=str(type(to_parse)))

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
