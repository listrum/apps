import json
from utils.https import Server
from methods.issue import Issue
from methods.send import Send
from components.nodeweb import NodeWeb
from components.tx_list import TxList
from components.storage import Storage


class Node(Server):

    def __init__(self) -> None:
        self.tx_list = TxList(3)
        self.nodes = []

    def start(self, certfile: str, keyfile: str, port: int = 2525) -> None:
        self.start_server(port, certfile,
                          keyfile)

    def set_owner(self, owner: str) -> None:
        self.owner = owner

    def set_storage(self, node: str,  dir: str = "listrum_storage") -> None:
        self.nodes.append(NodeWeb(node))
        self.storage = Storage(dir, node)

    def on_data(self, method: str, body):

        if method == "balance":
            return self.storage.get(body)

        # if method == "list":
        #     return self.tx_list.list

        if method == "issue":
            issue = Issue(body)

            issue.verify()
            issue.check_time()
            issue.check_owner(self.owner)

            self.tx_list.add(method, body)
            issue.add(self.storage)

            for node in self.nodes:
                node.issue(body)

        if method == "send":
            send = Send(body)

            send.verify()
            send.check_time()
            send.check_value(self.storage)

            self.tx_list.add(method, body)
            send.add_value(self.storage)

            for node in self.nodes:
                node.send(body)
