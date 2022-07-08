import json
import requests
from requests import Response

from components.constants import Const
from components.client import Client


class NodeReq:
    def __init__(self, address: str) -> None:

        if address.find(":") < 0:
            address += ":" + str(Const.port)

        self.address = "https://" + address

    def balance(self, wallet: str) -> float:
        res = requests.get(self.address + "/balance/" + wallet)
        return float(res.text)

    def send(self, tx: str) -> Response:
        return requests.get(self.address + "/send/" + tx)

    def history(self, wallet: str) -> Response:
        return requests.get(self.address + "/history/" + wallet)


class Nodes:
    def __init__(self) -> None:
        self.list = []

    def add_node(self, address: str) -> None:
        self.list.append(NodeReq(address))

    def remove_node(self, address: str) -> None:
        nodes = self.list

        for node in nodes:
            if node.address.find(address) >= 0:
                self.list.remove(node)

    def clear(self) -> None:
        self.list = []

    def send(self, tx) -> None:
        try:
            tx = json.dumps(tx)
        except:
            pass

        for node in self.list:
            node.send(tx)

    def balance(self, wallet: str) -> float:
        balance = 0
        nodes = 0

        for node in self.list:
            try:
                balance += node.balance(wallet)
                nodes += 1

            except:
                pass

        if not nodes:
            return 0

        return balance/nodes

    def client(self, pub: dict = {}) -> Client:
        cli = Client(pub)
        cli.set_nodes(self)

        return cli


def nodes_command(command: list, nodes: Nodes) -> None:
    if command[0] == "remove":
        nodes.remove_node(command[1])

    if command[0] in ["add", "node"]:
        nodes.add_node(command[1])

    if command[0] in ["list", "nodes"]:
        for node in nodes.list:
            print(node.address)

    if command[0] == "clear":
        nodes.list = []

    if command[0] in ["exit", "quit", "q", "close"]:
        exit()
