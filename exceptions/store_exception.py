class BaseStoreException(Exception):
    def __init__(self, message):
        self.message = message


class NoEntryError(BaseStoreException):
    def __init__(self, message):
        self.message = message


class DuplicateEntryError(BaseStoreException):
    def __init__(self, message):
        self.message = message


class DiskFullError(BaseStoreException):
    def __init__(self, message):
        self.message = message


class UnauthorizedRequestError(BaseStoreException):
    def __init__(self, message):
        self.message = message


class InvalidEntryNameError(BaseStoreException):
    def __init__(self, message):
        self.message = message