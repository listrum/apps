import os
from threading import Thread

from client.nodes import nodes
from client.constants import Const


class Storage:

    dir = "storage/"

    def __init__(self) -> None:
        try:
            os.makedirs(self.dir)
        except:
            pass

        self.res = []

    def get(self, wallet: str) -> float:
        try:
            with open(self.dir + wallet) as f:
                return float(f.read())

        except:
            if wallet in self.res:
                return 0.0

            Thread(target=self.from_node, args=(wallet,)).start()

            return 0.0

    def from_node(self, wallet: str) -> None:
        balance = nodes.balance(wallet)

        try:
            open(self.dir + wallet)
        except:
            self.res.append(wallet)

            if len(self.res) > Const.temp_storage_len:
                self.res.pop(0)

            if balance > 0.0:
                self.set(wallet, balance)

    def set(self, wallet: str, value: float) -> None:
        if not value:
            os.remove(self.dir + wallet)
            return

        with open(self.dir + wallet, "w") as f:
            f.write(str(value))

storage = Storage()