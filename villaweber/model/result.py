class ErrorResult():

    http_code = None
    message = None
    description = None

    def __init__(self, message) -> None:
        self.http_code = str
        self.message = message
        self.description = str

    def set_descriptiion(self, description) -> None:
        self.description = description

    def set_http_code(self, http_code) -> None:
        self.http_code = http_code
