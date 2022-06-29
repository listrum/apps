import json
import time
from components.errors import Error


class TxList:

    def __init__(self, max_length) -> None:
        self.list = []
        self.max_length = max_length

    def add(self, method_obj):
        # tx = "/" + method + "/" + json.dumps(body)

        if self.list.count(method_obj) > 0:
            raise Error("Already sent")

        if abs(self.list[0].time - time.time()) > 2000:
            self.list.pop(0)

        # if len(self.list) > self.max_length:
        #     # self.list = self.list[len(self.list) - self.max_length:]
        #     self.list = self.list[1:]

        self.list.append(method_obj)
