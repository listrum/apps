import json
from threading import Thread
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
        self.owner = ""

    def start(self, certfile: str, keyfile: str, port: int = 2525) -> None:
        self.start_server(port, certfile,
                          keyfile)

    def set_storage(self, node: str = "", dir: str = "node") -> None:
        self.storage = Storage(dir)

        if node:
            self.nodes.append(NodeWeb(node))
            self.storage.set_node(node)

    def add_node(self, address: str) -> None:
        self.nodes.append(NodeWeb(address))

    def remove_node(self, address: str) -> None:
        nodes = self.nodes

        for node in nodes:
            if node.address.find(address) >= 0:
                self.nodes.remove(node)

    def on_data(self, method: str, body):

        if method == "balance":
            return self.storage.get(body)

        if method == "issue":

            issue = Issue(body)

            issue.verify()

            issue.check_time()
            issue.check_owner(self.owner)

            self.tx_list.add(issue)
            issue.add(self.storage)

            for node in self.nodes:
                node.issue(body)

            return

        if method == "send":
            send = Send(body)

            send.verify()
            send.check_time()
            send.check_value(self.storage)

            self.tx_list.add(send)
            send.add_value(self.storage)

            for node in self.nodes:
                node.send(body)

            Thread(target=self.on_send, args=(send,)).start()

            return

        return self.new_method(method, body)

    def on_send(self, data: Send) -> None:
        pass

    def new_method(self, method: str, body):
        pass


def create_node(node: Node) -> Node:

    backup = input("Download node address (optional): ")
    path = input("Storage path (node/): ")
    if not path:
        path = "node"

    node.set_storage(backup, path)

    cert = input("Path to SSL certificate (keys/fullchain.pem): ")
    if not cert:
        cert = "keys/fullchain.pem"

    key = input("Path to SLL private key (keys/privkey.pem): ")
    if not key:
        key = "keys/privkey.pem"

    port = input("Node port (2525): ")
    if not port:
        port = 2525
    port = int(port)

    node.start(cert, key, port)

    print("Node started!")
    print("Command line:")

    return node


def check_command(node: Node, command: list) -> None:

    if command[0] in ["download", "main"]:
        try:
            node.storage.set_node(command[1])
        except:
            node.storage.set_node("")

    if command[0] in ["remove"]:
        node.remove_node(command[1])

    if command[0] in ["add", "node"]:
        node.add_node(command[1])

    if command[0] in ["list", "nodes"]:
        for web_node in node.nodes:
            print(web_node.address)

    if command[0] in ["owner"]:
        node.owner = command[1]


if __name__ == "__main__":
    node = Node()
    create_node(node)

    while True:
        command = input("/").split(" ")
        check_command(node, command)
