
class ServiceException(Exception):
    def __init__(self, message="Custom service exception occurred", original_exception=None):
        self.original_exception = original_exception
        super().__init__(message)
