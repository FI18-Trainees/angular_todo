class CreationError(Exception):
    def __init__(self, raw):
        super(CreationError, self).__init__()
        self.raw = raw
