import json
import os

from components.nodes import Nodes, nodes_command

from node_utils.repay import Repay
from node_utils.storage import Storage
from node_utils.tx_list import TxList
from node_utils.methods import check_balance, check_connect, check_connect_price, check_history, check_send

from utils.https import Server, Request


class Node(Server):
    def __init__(self) -> None:
        self.tx_list = TxList()
        self.nodes = Nodes()
        self.repay = Repay()

        with open("config.json") as f:
            self.config = json.loads(f.read())

        self.storage = Storage(self.config["storage"], self.nodes)
        self.wallet = self.config["wallet"]

        if self.config["node_connect"]["enabled"]:
            self.primary = Nodes()
            self.primary.add_node(self.config["node_connect"]["prime"])

            self.storage = Storage(self.storage.dir, self.primary)

        if self.config["history"]["enabled"]:
            if self.config["history"]["path"][-1] != "/":
                self.config["history"]["path"] += "/"

            try:
                os.makedirs(self.config["history"]["path"])
            except:
                pass

        self.start_server(
            self.config["port"], self.config["cert"], self.config["cert_key"])

        print("Node started!")

    def on_data(self, req: Request) -> None:
        check_balance(req, self)
        check_send(req, self)

        if self.config["history"]["enabled"]:
            check_history(req, self.config["history"]["path"])

        if self.config["node_connect"]["enabled"]:
            check_connect_price(req, self)
            check_connect(req, self)

        req.end("", 401)

    def issue(self, value: float) -> None:
        self.storage.set(self.wallet, self.storage.get(
            self.wallet) + float(value))


if __name__ == "__main__":
    node = Node()

    while 1:
        command = input("/").split(" ")

        try:
            if node.config["node_connect"]["enabled"]:
                nodes_command(command, node.primary)

            nodes_command(command, node.nodes)

            if command[0] in ["issue", "mint"]:

                node.issue(float(command[1]))

        except:
            pass
