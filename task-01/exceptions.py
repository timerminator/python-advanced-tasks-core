class RequestError(Exception):
    def __init__(self, message=None, status_code=None, payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def __str__(self):
        return f"RequestError: {self.message} (status: {self.status_code})"