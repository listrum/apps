import json
import requests
from requests import Response

from components.constants import Const


class NodeReq:
    def __init__(self, address: str) -> None:

        if address.find(":") < 0:
            address += ":" + Const.port_str

        self.address = "https://" + address

    def balance(self, owner: str) -> float:
        res = requests.get(self.address + "/balance/" + owner)
        return float(res.text)

    def send(self, body: str) -> Response:
        return requests.get(self.address + "/send/" + json.dumps(body))

    def history(self, owner: str) -> Response:
        return requests.get(self.address + "/history/" + owner)


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

    def send(self, data: str) -> None:
        for node in self.list:
            node.send(data)

    def balance(self, owner: str) -> float:
        balance = 0
        total = 0

        for node in self.list:
            try:
                balance += node.balance(owner)
                total += 1

            except:
                pass

        if not total:
            return 0

        return balance/total


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
