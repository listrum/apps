class Error(BaseException):
    def __init__(self, msg) -> None:
        self.msg = msg

    def __str__(self) -> str:
        return self.msg
