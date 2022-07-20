import json
import re
import requests
import os

from listrum.client.constants import Const


class NodeReq:
    def __init__(self, address: str) -> None:

        self.address = address

        if len(re.findall(r":[0-9]+$", address)) < 1:
            self.address += ":" + str(Const.port)

        if address.find("https://") < 0:
            self.address = "https://" + self.address

    def balance(self, wallet: str) -> float:
        res = requests.get(self.address + "/balance/" + str(wallet), timeout=3)
        return float(res.text)

    def send(self, tx: str):
        requests.get(self.address + "/send/" + str(tx), timeout=3)


class Nodes:
    def __init__(self) -> None:
        self.trusted = []
        self.broadcast = []

        self.update()

    def update(self) -> None:
        try:
            os.mkdir(os.path.expanduser("~") + "/listrum/")
        except:
            pass

        try:
            open(os.path.expanduser("~") + "/listrum/trusted_nodes.txt")
        except:
            open(os.path.expanduser("~") + "/listrum/trusted_nodes.txt", "w")

        try:
            open(os.path.expanduser("~") + "/listrum/broadcast_nodes.txt")
        except:
            open(os.path.expanduser("~") + "/listrum/broadcast_nodes.txt", "w")

        with open(os.path.expanduser("~") + "/listrum/trusted_nodes.txt") as f:
            for address in f.read().split("\n"):
                if address:
                    self.trusted.append(NodeReq(address))

        with open(os.path.expanduser("~") + "/listrum/broadcast_nodes.txt") as f:
            for address in f.read().split("\n"):
                if address:
                    self.broadcast.append(NodeReq(address))

    def send(self, tx) -> None:
        tx = json.dumps(tx.data)

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
        sources = 0


        for node in self.trusted:
            try:
                balance += node.balance(wallet)
                sources += 1

            except BaseException as b:
                print("Unable get balance from " + node.address)

        if not sources:
            return 0.0

        return balance/sources


nodes = Nodes()