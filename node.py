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


if __name__ == "__main__":
    node = Node()

    backup = input("Backup node address (node.listrum.com): ")
    if not backup:
        backup = "node.listrum.com"

    path = input("Storage path (node/): ")
    if not path:
        path = "node"

    node.set_storage(backup, path)

    owner = input("Owner address (gO5qyZHrd17GlFsuH): ")
    if not owner:
        owner = "gO5qyZHrd17GlFsuH"

    node.set_owner(owner)

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
