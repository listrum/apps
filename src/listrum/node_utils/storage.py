import os
from threading import Thread

from components.nodes import Nodes
from components.constants import Const


class Storage:

    def __init__(self, dir: str) -> None:
        if dir[-1:] != "/":
            dir += "/"

        try:
            os.makedirs(dir)
        except:
            pass

        self.dir = dir
        self.nodes = Nodes()
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
        balance = self.nodes.balance(wallet)

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
