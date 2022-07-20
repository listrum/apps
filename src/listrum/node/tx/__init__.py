import json
import time

from client.constants import Const
from client.error import Error
from client.crypto import pad_key, verify

from node.tx.storage import Storage


class Tx:

    def __init__(self, params: dict) -> None:

        self.data = params["data"]
        self.to = str(params["data"]["to"])
        self.value = float(params["data"]["value"])

        self.pub = str(params["from"]["pub"])
        self.wallet = str(pad_key(self.pub))
        self.time = int(params["from"]["time"])
        self.sign = str(params["from"]["sign"])

        self.storage = Storage()

    def verify(self) -> None:
        verify(self.pub, json.dumps(self.data).replace(
            " ", "") + str(self.time), self.sign)

    def check_time(self) -> None:
        if abs(time.time()*1000 - self.time) > Const.tx_ttl:
            raise Error("Outdated")

    def check_value(self) -> None:
        self.from_value = self.storage.get(self.wallet)

        if self.value <= 0:
            raise Error("WrongValue")

        if self.from_value < self.value:
            raise Error("NotEnough")

    def add_value(self) -> None:

        self.storage.set(self.wallet, self.from_value - self.value)
        self.storage.set(self.to, self.storage.get(self.to) + self.value*Const.fee)