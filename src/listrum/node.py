import json
import os
import signal
from threading import Thread

from components.nodes import Nodes
from node_utils.send import Send

from node_utils.repay import Repay
from node_utils.storage import Storage
from node_utils.tx_list import TxList
from node_utils.methods import check_balance, check_send, check_fee

from utils.https import Server, Request


class Node(Server):

    def __init__(self) -> None:
        self.tx_list = TxList()
        self.nodes = Nodes()
        self.repay = Repay()

        with open("node_config.json") as f:
            self.config = json.loads(f.read())

        self.storage = Storage(self.config["storage"])
        self.wallet = self.config["wallet"]

        self.start_server(
            self.config["port"], self.config["cert"], self.config["cert_key"])

        self.command()

    def on_data(self, req: Request) -> None:
        check_balance(req, self)
        check_send(req, self)
        check_fee(req)

        req.end("", 401)

    def issue(self, value: float) -> None:
        self.storage.set(self.wallet, self.storage.get(
            self.wallet) + float(value))

    def on_send(self, tx: Send) -> None:
        pass

    def command(self) -> None:

        print("Node started!")

        def check_command() -> None:
            while 1:
                command = input("/").split(" ")

                try:
                    if command[0] in ["update", "upgrade", "reload"]:
                        self.nodes.update()

                    if command[0] in ["exit", "quit", "q", "close"]:
                        os.kill(os.getpid(), signal.SIGUSR1)

                    if command[0] in ["issue", "mint"]:
                        node.issue(float(command[1]))

                except:
                    pass

        Thread(target=check_command).start()


if __name__ == "__main__":
    node = Node()
