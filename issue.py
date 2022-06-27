import json
from errors import Error
import time
from crypto import verify
from crypto import pad_key
from storage import Storage


class Issue:
    def __init__(self, params: dict) -> None:
        self.owner = params["from"]["owner"]
        self.key = pad_key(self.owner)
        self.time = int(params["from"]["time"])
        self.sign = params["from"]["sign"]
        self.value = int(params["value"])

    def verify(self) -> None:
        verify(self.owner, '"' + str(self.value) +
               '"' + str(self.time), self.sign)

    def check_time(self) -> None:
        if abs(time.time()*1000 - self.time) > 2000:
            raise Error("Outdated")

    def check_owner(self, owner: str) -> None:
        if owner != self.key:
            raise Error("NotOwner")

    def add(self, storage: Storage) -> None:
        storage.set(self.key, storage.get(self.key) + self.value)
