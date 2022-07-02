from components.constants import Const
from methods.issue import check_issue
from methods.send import check_send
from methods.balance import check_balance

from node_prototype import NodePrototype
from utils.https import Request


class Node(NodePrototype):

    def on_data(self, req: Request):

        check_balance(req, self)
        check_issue(req, self)
        check_send(req, self)


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

    port = input("Node port (" + Const.port_str + "): ")
    if not port:
        port = Const.port
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
