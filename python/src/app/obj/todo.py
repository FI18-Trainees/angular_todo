import dateutil.parser

from utils import Console
from .errors import CreationError, DataMissingError, InvalidValueError, InvalidInputTypeError
from .sql_types import SQLTodo

SHL = Console("Todo")


def return_raw(raw):
    return raw


def get_value_and_parse(raw, key_attribute: str, parse_method, optional: bool = True, default=None):
    if isinstance(raw, dict):
        try:
            value = raw[key_attribute]
        except KeyError:
            value = default
            if not optional:
                SHL.error(f"Failed creating Todo. Mandatory key '{key_attribute}' missing.")
                raise DataMissingError(missing_key=key_attribute)
    else:
        try:
            value = raw.__getattribute__(key_attribute)
        except AttributeError:
            value = default
            if not optional:
                SHL.error(f"Failed creating Todo. Mandatory key '{key_attribute}' missing.")
                raise DataMissingError(missing_key=key_attribute)

    if value is not None:
        try:
            value = parse_method(value)
            if parse_method == str:
                if value.strip().lower() in ["none", "null", ""]:
                    SHL.error(f"Failed creating Todo. Invalid key '{key_attribute}' provided.")
                    raise InvalidValueError(name_of_invalid=key_attribute)
            return value
        except ValueError:
            SHL.error(f"Failed creating Todo. Invalid key '{key_attribute}' provided.")
            raise InvalidValueError(name_of_invalid=key_attribute)
        except TypeError:
            SHL.error(f"Failed creating Todo. Invalid key '{key_attribute}' provided.")
            raise InvalidValueError(name_of_invalid=key_attribute)
    else:
        if isinstance(raw, SQLTodo):
            return None
        if optional:
            return default
        else:
            SHL.error(f"Failed creating Todo. Mandatory key '{key_attribute}' missing.")
            raise DataMissingError(missing_key=key_attribute)


class Todo:
    def __init__(self, to_parse):
        if any([isinstance(to_parse, x) for x in [dict, SQLTodo]]):  # check for valid inputs
            # mandatory
            self.title = get_value_and_parse(to_parse, "title", parse_method=str, optional=False)
            self.finished = get_value_and_parse(to_parse, "finished", parse_method=bool, optional=False)
            self.list_id = get_value_and_parse(to_parse, "list_id", parse_method=int, optional=False)

            # optional
            self.address = get_value_and_parse(to_parse, "address", parse_method=str)
            self.description = get_value_and_parse(to_parse, "description", parse_method=str)
            self.subtasks = get_value_and_parse(to_parse, "subtasks", parse_method=str)
            self.priority = get_value_and_parse(to_parse, "priority", parse_method=int, default=0)

            if isinstance(to_parse, dict):
                self.item_id = get_value_and_parse(to_parse, "item_id", parse_method=int)
                self.due_date = get_value_and_parse(to_parse, "due_date", parse_method=dateutil.parser.isoparse)
                self.reminder = get_value_and_parse(to_parse, "reminder", parse_method=dateutil.parser.isoparse)
            else:
                self.item_id = get_value_and_parse(to_parse, "item_id", parse_method=int, optional=False)
                self.due_date = get_value_and_parse(to_parse, "due_date", parse_method=return_raw)
                self.reminder = get_value_and_parse(to_parse, "reminder", parse_method=return_raw)
        else:
            SHL.error(f"Failed creating Todo. Invalid internal input type.")
            SHL.error(f"Type provided: {type(to_parse)}")
            raise InvalidInputTypeError(type_provided=str(type(to_parse)))

    def to_json(self) -> dict:
        return {
            "item_id": int(self.item_id),
            "list_id": int(self.list_id),
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
            list_id=int(self.list_id),
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
