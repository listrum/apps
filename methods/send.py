import json
import time
from utils.crypto import pad_key, verify
from components.errors import Error
from components.storage import Storage


class Send:

    def __init__(self, params: dict) -> None:
        self.tx_list = list(params["to"])
        self.owner = str(params["from"]["owner"])
        self.key = str(pad_key(self.owner))
        self.time = int(params["from"]["time"])
        self.sign = str(params["from"]["sign"])

    def verify(self) -> None:
        verify(self.owner, json.dumps(self.tx_list).replace(
            " ", "") + str(self.time), self.sign)

    def check_time(self) -> None:
        if abs(time.time()*1000 - self.time) > 2000:
            raise Error("Outdated")

    def check_value(self, storage: Storage) -> None:
        self.from_value = storage.get(self.key)

        self.to_value = 0

        for tx in self.tx_list:

            if int(tx["value"]) <= 0:
                raise Error("WrongValue")

            self.to_value += int(tx["value"])

        if self.from_value < self.to_value:
            raise Error("NotEnough")

    def add_value(self, storage: Storage) -> None:

        storage.set(self.key, self.from_value - self.to_value)

        for tx in self.tx_list:
            storage.set(tx["to"], storage.get(tx["to"]) + int(tx["value"]))
