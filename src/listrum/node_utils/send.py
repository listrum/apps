import json
import time

from components.constants import Const
from components.error import Error

from node_utils.storage import Storage

from utils.crypto import pad_key, verify

from node_prototype import NodePrototype


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
