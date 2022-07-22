import os
import signal
from threading import Thread

from listrum.node.tx.repay import Repay
from listrum.node.tx.storage import storage
from listrum.node.tx.list import TxList
from listrum.node.tx import Tx
from listrum.node.balance import check_balance
from listrum.node.fee import check_fee
from listrum.node import config

from listrum.client.https import Server, Request
from listrum.client import nodes


class Node(Server):

    def __init__(self) -> None:
        self.tx_list = TxList()
        self.repay = Repay()

        self.start_server(
            config.port, config.cert, config.cert_key)

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
            nodes.send(tx.params)

        self.on_request(req)

        req.end("", 401)

    def issue(self, value: float) -> None:
        storage.set(config.wallet, storage.get(config.wallet) + float(value))

    def on_send(self, tx: Tx) -> None:
        pass

    def on_request(self, req: Request) -> None:
        pass

    def command(self) -> None:

        print("Node started!")

        def check_command() -> None:
            while 1:
                command = input("/").split(" ")

                try:
                    if command[0] in ["update", "upgrade", "reload"]:
                        nodes.update()
                        print("Nodes updated!")

                    if command[0] in ["exit", "quit", "q", "close"]:
                        os.kill(os.getpid(), signal.SIGUSR1)

                    if command[0] in ["issue", "mint", "add"]:
                        self.issue(float(command[1]))

                except:
                    pass

        Thread(target=check_command).start()
