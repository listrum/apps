import os
from re import A
from threading import Thread
from components.node_req import NodeReq


class Storage:

    def __init__(self, dir: str) -> None:
        if dir[-1:] != "/":
            dir += "/"

        try:
            os.makedirs(dir)
        except:
            pass

        self.dir = dir
        self.node = ""

    def get(self, owner: str) -> float:
        try:
            with open(self.dir + owner) as f:
                return float(f.read())

        except:
            if self.node:
                Thread(target=self.from_node, args=(owner,)).start()

            return 0.0

    def set_node(self, address: str) -> None:
        if address:
            self.node = NodeReq(address)
        else:
            self.node = ""

    def from_node(self, owner: str) -> str:
        balance = self.node.balance(owner)

        try:
            open(self.dir + owner)
        except:
            if balance > 0.0:
                self.set(owner, balance)

    def set(self, owner: str, value: int) -> None:

        with open(self.dir + owner, "w") as f:
            f.write(str(value))
