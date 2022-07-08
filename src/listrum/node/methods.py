import json
import time

from node.storage import Storage
from node.node_prototype import NodePrototype
from components.constants import Const
from components.error import Error
from utils.https import Request
from utils.crypto import pad_key, verify


def check_balance(req: Request, node: NodePrototype) -> None:
    if req.method != "balance":
        return

    req.end(node.storage.get(req.body))


def check_send(req: Request, node: NodePrototype) -> None:
    if req.method != "send":
        return

    send = Send(req.body)

    print(send.to, send.wallet, send.value)

    send.verify()
    send.check_time()
    send.check_value(node.storage)
    send.repay(node)

    node.tx_list.add(send)
    send.add_value(node.storage)

    node.nodes.send(req.body)

    # print(send.to, send.value)

    # req.end(send.value*Const.fee)
    req.end()

    print(1)


class Send:

    def __init__(self, params: dict) -> None:

        self.data = params["data"]
        self.to = str(params["data"]["to"])
        self.value = float(params["data"]["value"])

        self.pub = str(params["from"]["pub"])
        self.wallet = str(pad_key(self.pub))
        self.time = int(params["from"]["time"])
        self.sign = str(params["from"]["sign"])

    def verify(self) -> None:
        verify(self.pub, json.dumps(self.data).replace(
            " ", "") + str(self.time), self.sign)

    def check_time(self) -> None:
        if abs(time.time()*1000 - self.time) > Const.tx_ttl:
            raise Error("Outdated")

    def check_value(self, storage: Storage) -> None:
        self.from_value = storage.get(self.wallet)

        if self.value <= 0:
            raise Error("WrongValue")

        if self.from_value < self.value:
            # print(1)
            raise Error("NotEnough")

    def add_value(self, storage: Storage) -> None:

        storage.set(self.wallet, self.from_value - self.value)
        storage.set(self.to, storage.get(
            self.to) + self.value*Const.fee)

    def repay(self, node: NodePrototype) -> None:
        self.from_value += node.repay.add(self.value)