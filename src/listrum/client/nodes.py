import json
import re
import requests
import os

from listrum.node import config


class NodeReq:
    def __init__(self, address: str) -> None:

        address = address

        if len(re.findall(r":[0-9]+$", address)) < 1:
            address += ":" + str(config.port)

        if address.find("https://") < 0:
            address = "https://" + address

    def balance(self, wallet: str) -> float:
        res = requests.get(self.address + "/balance/" + str(wallet), timeout=3)
        return float(res.text)

    def send(self, tx: str):
        requests.get(self.address + "/send/" + str(tx), timeout=3)


path = os.path.expanduser("~") + "/listrum/"
trusted = []
broadcast = []


def update() -> None:

    try:
        open(path + "trusted_nodes.txt")
    except:
        open(path + "trusted_nodes.txt", "w")

    try:
        open(path + "broadcast_nodes.txt")
    except:
        open(path + "broadcast_nodes.txt", "w")

    with open(path + "trusted_nodes.txt") as f:
        for address in f.read().split("\n"):
            if address:
                trusted.append(NodeReq(address))

    with open(path + "broadcast_nodes.txt") as f:
        for address in f.read().split("\n"):
            if address:
                broadcast.append(NodeReq(address))

    if not trusted:
        print("No trusted! Add in your user dir /listrum/trusted_nodes.txt")


def send(tx: dict) -> None:
    tx = json.dumps(tx)

    for node in broadcast:
        try:
            node.send(tx)
        except:
            print("Unable to send to " + node.address)

    for node in trusted:
        try:
            node.send(tx)
        except:
            print("Unable to send to " + node.address)


def balance(wallet: str) -> float:
    total_balance = 0
    sources = 0

    balance = 0
    for node in trusted:
        try:
            balance = node.balance(wallet)

            if balance >= 0:
                total_balance += balance
                sources += 1

        except BaseException as b:
            print("Unable get balance from " + node.address)

    if not sources:
        return 0.0

    return balance/sources


try:
    os.makedirs(path)
except:
    pass
update()
