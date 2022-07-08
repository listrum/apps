import os
from threading import Thread


class Storage:

    def __init__(self, dir: str, node) -> None:
        if dir[-1:] != "/":
            dir += "/"

        try:
            os.makedirs(dir)
        except:
            pass

        self.dir = dir
        self.node = node

    def get(self, wallet: str) -> float:
        try:
            with open(self.dir + wallet) as f:
                return float(f.read())

        except:
            Thread(target=self.from_node, args=(wallet,)).start()

            return 0.0

    def from_node(self, wallet: str) -> None:
        balance = self.node.nodes.balance(wallet)

        try:
            open(self.dir + wallet)
        except:
            if balance > 0.0:
                self.set(wallet, balance)

    def set(self, wallet: str, value: float) -> None:

        if not value:
            os.remove(self.dir + wallet)
            return

        with open(self.dir + wallet, "w") as f:
            f.write(str(value))
