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
        verify(self.owner, json.dumps(self.data).replace(
            " ", "") + str(self.time), self.sign)

    def check_time(self) -> None:
        if abs(time.time()*1000 - self.time) > 2000:
            raise Error("Outdated")

    def check_value(self, storage: Storage) -> None:
        self.from_value = storage.get(self.key)

        if self.value <= 0:
            raise Error("WrongValue")

        if self.from_value < self.value:
            raise Error("NotEnough")

    def add_value(self, storage: Storage) -> None:

        storage.set(self.key, self.from_value - self.value)

        storage.set(self.to, storage.get(
            self.to) + self.value)
