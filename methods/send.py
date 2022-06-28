import json
import time
from utils.crypto import pad_key, verify
from components.errors import Error
from components.storage import Storage


class Send:

    def __init__(self, params: dict) -> None:
        self.data = params["to"]
        self.to = str(params["to"]["to"])
        self.value = int(params["to"]["value"])

        self.owner = str(params["from"]["owner"])
        self.key = str(pad_key(self.owner))
        self.time = int(params["from"]["time"])
        self.sign = str(params["from"]["sign"])

    def verify(self) -> None:
        verify(self.owner, json.dumps(self.data) + str(self.time), self.sign)

    def check_time(self) -> None:
        if abs(time.time()*1000 - self.time) > 2000:
            raise Error("Outdated")

    def check_value(self, storage: Storage) -> None:
        self.from_value = storage.get(self.key)

        # self.to_value = int(self.tx_list["value"])

        # for tx in self.tx_list:

        if self.value <= 0:
            raise Error("WrongValue")

        #     self.to_value += int(tx["value"])
        print(1)
        if self.from_value < self.value:
            raise Error("NotEnough")

    def add_value(self, storage: Storage) -> None:

        storage.set(self.key, self.from_value - self.value)

        # for tx in self.tx_list:
        storage.set(self.to, storage.get(
            self.to) + self.value)
