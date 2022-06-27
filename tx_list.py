import json
from errors import Error


class TxList:

    def __init__(self, max_length) -> None:
        self.list = []
        self.max_length = max_length

    def add(self, method, body):
        tx = "/" + method + "/" + json.dumps(body)

        if self.list.count(tx) > 0:
            raise Error("Already sent")

        if len(self.list) > self.max_length:
            # self.list = self.list[len(self.list) - self.max_length:]
            self.list = self.list[1:]

        self.list.append(tx)
