import json
import time
import os

from listrum.components.constants import Const
from listrum.components.nodes import Nodes, nodes_command
from components.error import Error

from node_utils.repay import Repay
from node_utils.storage import Storage
from node_utils.tx_list import TxList

from utils.https import Server, Request
from utils.crypto import pad_key, verify


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
            self.primary.add_node("127.0.0.1:" + self.config["port"])

            self.storage = Storage(self.storage.dir, self.primary)

        if self.config["history"]["enabled"]:
            try:
                os.makedirs(self.config["history"]["path"])
            except:
                pass

        self.start_server(
            int(self.config["port"]), self.config["cert"], self.config["cert_key"])

        print("Node started!")

    def on_data(self, req: Request) -> None:
        check_balance(req, self)
        check_send(req, self)

        if self.config["history"]["enabled"]:
            check_history(req, self.config["history"]["path"])

        if self.config["node_connect"]["enabled"]:
            check_connect(req, self)

        req.end("", 401)

    def issue(self, value: int) -> None:
        self.storage.set(self.wallet, self.storage.get(
            self.wallet) + float(value))


if __name__ == "__main__":
    node = Node()

    while 1:
        command = input("/").split(" ")

        try:
            if node.config["node_connect"]["enabled"]:
                nodes_command(command, node.primary)
            else:
                nodes_command(command, node.nodes)

            if command[0] in ["issue", "mint"]:
                try:
                    node.issue(command[1], float(command[2]))
                except:
                    node.issue(command[2], float(command[1]))

        except:
            pass


def check_connect(req: Request, self: Node) -> None:
    if req.method != "connect":
        return

    value = self.primary.client(req.body["from"])
    temp_wallet = self.primary.client()

    value.send_all(temp_wallet.wallet)

    if temp_wallet.balance() < float(self.config["node_connect"]["price"])/Const.fee*Const.fee*Const.fee:
        raise Error("Bad price")

    temp_wallet.send_all(self.wallet)

    self.nodes.add_node(req.body["data"])

    req.end()


def check_history(req: Request, history_path: str) -> None:
    if req.method == "send":
        from_wallet = pad_key(req.body["from"]["pub"])
        to_wallet = req.body["data"]["to"]

        try:
            with open(history_path + from_wallet) as f:
                history_from = f.readlines()
        except:
            history_from = []

        try:
            with open(history_path + to_wallet) as f:
                history_to = f.readlines()
        except:
            history_to = []

        history_from.append(json.dumps(req.body["data"]) + "\n")
        history_to.append(json.dumps(req.body["data"]) + "\n")

        if len(history_from) > Const.history_len:
            history_from.pop(0)
        if len(history_to) > Const.history_len:
            history_to.pop(0)

        with open(history_path + from_wallet, "w") as f:
            f.writelines(history_from)

        with open(history_path + to_wallet, "w") as f:
            f.writelines(history_to)

    if req.method == "history":
        try:
            with open(history_path + req.body) as f:
                req.end(f.readlines())

        except:
            req.end([])


def check_balance(req: Request, node: Node) -> None:
    if req.method != "balance":
        return

    req.end(node.storage.get(req.body))


def check_send(req: Request, node: Node) -> None:
    if req.method != "send":
        return

    send = Send(req.body)

    # print(send.to, send.wallet, send.value)

    send.verify()
    send.check_time()
    send.check_value(node.storage)
    send.repay(node)

    node.tx_list.add(send)

    send.add_value(node.storage)

    req.end()

    node.nodes.send(req.body)

    # print(send.to, send.value)

    # print(1)


class Send:

    def __init__(self, params: dict) -> None:

        self.data = params["data"]
        self.to = str(params["data"]["to"])
        self.value = float(params["data"]["value"])

        self.pub = str(params["from"]["pub"])
        self.wallet = str(pad_key(self.pub))
        self.time = int(params["from"]["time"])
        self.sign = str(params["from"]["sign"])

    def verify(self) -> None:
        verify(self.pub, json.dumps(self.data).replace(
            " ", "") + str(self.time), self.sign)

    def check_time(self) -> None:
        if abs(time.time()*1000 - self.time) > Const.tx_ttl:
            raise Error("Outdated")

    def check_value(self, storage: Storage) -> None:
        self.from_value = storage.get(self.wallet)

        if self.value <= 0:
            raise Error("WrongValue")

        if self.from_value < self.value:
            # print(1)
            raise Error("NotEnough")

    def add_value(self, storage: Storage) -> None:

        storage.set(self.wallet, self.from_value - self.value)
        storage.set(self.to, storage.get(
            self.to) + self.value*Const.fee)

    def repay(self, node: Node) -> None:
        self.from_value += node.repay.add(self.value)
