import time
from components.constants import Const
from components.errors import Error


class TxList:

    def __init__(self) -> None:
        self.list = []

    def add(self, method_obj):

        for method in self.list:
            if method.sign == method_obj.sign:
                raise Error("Already sent")

        self.list.append(method_obj)

        if abs(self.list[0].time - time.time()*1000) > Const.tx_ttl:
            self.list.pop(0)
