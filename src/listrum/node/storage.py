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

    def get(self, owner: str) -> float:
        try:
            with open(self.dir + owner) as f:
                return float(f.read())

        except:
            Thread(target=self.from_node, args=(owner,)).start()

            return 0.0

    def from_node(self, owner: str) -> None:
        balance = self.node.nodes.balance(owner)

        try:
            open(self.dir + owner)
        except:
            if balance > 0.0:
                self.set(owner, balance)

    def set(self, owner: str, value: float) -> None:

        if not value:
            os.remove(self.dir + owner)
            return

        with open(self.dir + owner, "w") as f:
            f.write(str(value))
