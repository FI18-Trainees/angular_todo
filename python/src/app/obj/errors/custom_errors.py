class CreationError(Exception):
    def __init__(self):
        super(CreationError, self).__init__()

    def get_error_message(self) -> str:
        return "Failed creating object."


class DataMissingError(CreationError):
    def __init__(self, missing_key):
        super(DataMissingError, self).__init__()
        self.missing_key = missing_key

    def get_error_message(self) -> str:
        return f"Failed creating object. '{self.missing_key}' missing."


class InvalidValueError(CreationError):
    def __init__(self, name_of_invalid):
        super(InvalidValueError, self).__init__()
        self.name_of_invalid = name_of_invalid

    def get_error_message(self) -> str:
        return f"Failed creating object. Value for '{self.name_of_invalid}' is invalid."


class InvalidInputTypeError(CreationError):
    def __init__(self, type_provided):
        super(InvalidInputTypeError, self).__init__()
        self.type_provided = type_provided

    def get_error_message(self) -> str:
        return f"Failed creating object. Invalid input type '{self.type_provided}'"


class DatabaseError(Exception):
    def __init__(self, original_error):
        super(DatabaseError, self).__init__()
        self.original_error = original_error
