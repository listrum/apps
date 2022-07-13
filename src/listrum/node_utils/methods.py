import json
import time
import os

from components.constants import Const
from components.nodes import Nodes, nodes_command
from components.error import Error

from node_utils.repay import Repay
from node_utils.storage import Storage
from node_utils.tx_list import TxList

from utils.https import Server, Request
from utils.crypto import pad_key, verify

from node_prototype import NodePrototype


def check_connect(req: Request, self: NodePrototype) -> None:
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


def check_balance(req: Request, node: NodePrototype) -> None:
    if req.method != "balance":
        return

    req.end(node.storage.get(req.body))


def check_send(req: Request, node: NodePrototype) -> None:
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
