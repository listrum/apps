import json
import os
import signal
from threading import Thread

from node.tx.repay import Repay
from node.tx.storage import storage
from node.tx.list import TxList
from node.tx import Tx
from node.balance import check_balance
from node.fee import check_fee

from client.https import Server, Request
from client.nodes import nodes

class Node(Server):

    def __init__(self) -> None:
        self.tx_list = TxList()
        self.repay = Repay()

        with open("node_config.json") as f:
            self.config = json.loads(f.read())

        self.wallet = self.config["wallet"]

        self.start_server(
            self.config["port"], self.config["cert"], self.config["cert_key"])

        self.command() 

    def on_data(self, req: Request) -> None:
        check_balance(req)
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
            nodes.send(tx)

        req.end("", 401)

    def issue(self, value: float) -> None:
        storage.set(self.wallet, storage.get(self.wallet) + float(value))

    def on_send(self, tx: Tx) -> None:
        pass

    def command(self) -> None:

        print("Node started!")

        def check_command() -> None:
            while 1:
                command = input("/").split(" ")

                try:
                    if command[0] in ["update", "upgrade", "reload"]:
                        nodes.update()

                    if command[0] in ["exit", "quit", "q", "close"]:
                        os.kill(os.getpid(), signal.SIGUSR1)

                    if command[0] in ["issue", "mint", "add"]:
                        self.issue(float(command[1]))

                except:
                    pass

        Thread(target=check_command).start()


if __name__ == "__main__":
    Node()
