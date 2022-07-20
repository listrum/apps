import json
import os
import signal
from threading import Thread

from listrum.client.nodes import Nodes
from listrum.node.tx.send import Send

from node.tx.repay import Repay
from node.tx.storage import Storage
from node.tx.list import TxList

from node.balance import check_balance
from node.tx import Tx, check_tx
from node.fee import check_fee

from listrum.client.https import Server, Request


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
        check_fee(req)

        if req.method == "send":
            tx = Tx(req.body)

            tx.verify()
            tx.check_time()
            tx.check_value()

            tx.from_value += self.repay.add(tx.value)
            self.tx_list.add(tx)
            tx.add_value()

            req.end()

            self.on_send(tx)
            self.nodes.send(tx)

        req.end("", 401)

    def issue(self, value: float) -> None:
        self.storage.set(self.wallet, self.storage.get(
            self.wallet) + float(value))

    def on_send(self, tx: Tx) -> None:
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
                        self.issue(float(command[1]))

                except:
                    pass

        Thread(target=check_command).start()


if __name__ == "__main__":
    Node()
