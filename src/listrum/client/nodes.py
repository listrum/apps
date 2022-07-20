import json
import re
import requests

from constants import Const


class NodeReq:
    def __init__(self, address: str) -> None:

        self.address = address

        if len(re.findall(r":[0-9]+$", address)) < 1:
            self.address += ":" + str(Const.port)

        if address.find("https://") < 0:
            self.address = "https://" + self.address

    def balance(self, wallet: str) -> float:
        res = requests.get(self.address + "/balance/" + wallet, timeout=3)
        return float(res.text)

    def send(self, tx: str):
        requests.get(self.address + "/send/" + tx, timeout=3)


class Nodes:
    def __init__(self) -> None:
        self.trusted = []
        self.broadcast = []

        self.update()

    def update(self) -> None:
        with open("trusted_nodes.txt") as f:
            for address in f.read().split("\n"):
                if address:
                    self.trusted.append(NodeReq(address))

        with open("broadcast_nodes.txt") as f:
            for address in f.read().split("\n"):
                if address:
                    self.broadcast.append(NodeReq(address))

    def send(self, tx) -> None:
        try:
            tx = json.dumps(tx)
        except:
            pass

        for node in self.broadcast:
            try:
                node.send(tx)
            except:
                print("Unable to send to " + node.address)

        for node in self.trusted:
            try:
                node.send(tx)
            except:
                print("Unable to send to " + node.address)

    def balance(self, wallet: str) -> float:
        balance = 0
        nodes = 0

        for node in self.trusted:
            try:
                balance += node.balance(wallet)
                nodes += 1

            except:
                print("Unable get balance from " + node.address)

        if not nodes:
            return 0.0

        return balance/nodes
