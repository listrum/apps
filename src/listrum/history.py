import json
import os
from listrum.components.constants import Const

from methods import check_balance,Send, check_send
from node import create_node, check_command
from node_prototype import NodePrototype
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
        from_key = pad_key(req.body["from"]["owner"])
        to_key = req.body["to"]["to"]

        try:
            with open(node.history_path + from_key) as f:
                history_from = f.readlines()
        except:
            history_from = []

        try:
            with open(node.history_path + to_key) as f:
                history_to = f.readlines()
        except:
            history_to = []

        history_from.append(json.dumps(req.body["to"]) + "\n")
        history_to.append(json.dumps(req.body["to"]) + "\n")

        if len(history_from) > Const.history_len:
            history_from.pop(0)
        if len(history_to) > Const.history_len:
            history_to.pop(0)

        with open(node.history_path + from_key, "w") as f:
            f.writelines(history_from)

        with open(node.history_path + to_key, "w") as f:
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
        check_command(node, command)

        if command[0] == "history":
            node.history(command[1])
