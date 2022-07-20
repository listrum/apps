import json
import time

from listrum.client.constants import Const
from listrum.client.error import Error
from listrum.client.crypto import pad_key, verify

from listrum.node.tx.storage import storage


class Tx:

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

    def check_value(self) -> None:
        self.from_value = storage.get(self.wallet)

        if self.value <= 0:
            raise Error("WrongValue")

        if self.from_value < self.value:
            raise Error("NotEnough")

    def add_value(self) -> None:

        storage.set(self.wallet, self.from_value - self.value)
        storage.set(self.to, storage.get(self.to) + self.value*Const.fee)