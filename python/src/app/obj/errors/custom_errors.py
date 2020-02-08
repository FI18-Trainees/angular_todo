class CreationError(Exception):
    def __init__(self, raw):
        super(CreationError, self).__init__()
        self.raw = raw


class DatabaseError(Exception):
    def __init__(self, original_error):
        super(DatabaseError, self).__init__()
        self.original_error = original_error
