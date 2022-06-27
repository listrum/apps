import os
from threading import Thread

from components.nodeweb import NodeWeb


class Storage:

    def __init__(self, dir: str, node: str) -> None:
        if dir[-1:] != "/":
            dir += "/"

        try:
            os.mkdir(dir)
        except:
            pass

        self.dir = dir
        self.node = NodeWeb(node)

    def get(self, owner: str) -> int:
        try:
            with open(self.dir + owner) as f:
                return int(f.read())

        except:
            Thread(target=self.from_node, args=(owner,)).start()

            return 0

    def from_node(self, owner: str) -> str:
        balance = self.node.balance(owner)
        try:
            open(self.dir + owner)
        except:
            self.set(owner, balance)

    def set(self, owner: str, value: int) -> None:

        with open(self.dir + owner, "w") as f:
            f.write(str(value))
