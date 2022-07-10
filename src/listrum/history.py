import json
import os
from components.constants import Const
from components.nodes import nodes_command

from node.methods import check_balance, check_send
from node import create_node
from node.node_prototype import NodePrototype
from utils.crypto import pad_key
from utils.https import Request


class History(NodePrototype):

    def on_data(self, req: Request) -> None:

        check_balance(req, self)
        check_send(req, self)
        check_history(req, self)

        req.end("", 401)

    def history(self, path: str) -> None:
        if path[-1:] != "/":
            path += "/"

        try:
            os.makedirs(path)
        except:
            pass

        self.history_path = path


def check_history(req: Request, node: History) -> None:
    if req.method == "send":
        from_wallet = pad_key(req.body["from"]["pub"])
        to_wallet = req.body["data"]["to"]

        try:
            with open(node.history_path + from_wallet) as f:
                history_from = f.readlines()
        except:
            history_from = []

        try:
            with open(node.history_path + to_wallet) as f:
                history_to = f.readlines()
        except:
            history_to = []

        history_from.append(json.dumps(req.body["data"]) + "\n")
        history_to.append(json.dumps(req.body["data"]) + "\n")

        if len(history_from) > Const.history_len:
            history_from.pop(0)
        if len(history_to) > Const.history_len:
            history_to.pop(0)

        with open(node.history_path + from_wallet, "w") as f:
            f.writelines(history_from)

        with open(node.history_path + to_wallet, "w") as f:
            f.writelines(history_to)

    if req.method == "history":
        try:
            with open(node.history_path + req.body) as f:
                req.end(f.readlines())

        except:
            req.end([])


if __name__ == "__main__":
    node = History()

    path = input("History path: ")
    if not path:
        path = "history"

    node.history(path)
    create_node(node)

    while True:
        command = input("/").split(" ")

        try:
            nodes_command(command, node.nodes)

            if command[0] in ["issue", "mint"]:
                try:
                    node.issue(command[1], float(command[2]))
                except:
                    node.issue(command[2], float(command[1]))
        except:
            pass
