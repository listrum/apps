from components.constants import Const
from components.nodes import nodes_command
from node.methods import check_send, check_balance
from node.node_prototype import NodePrototype
from utils.https import Request


class Node(NodePrototype):

    def on_data(self, req: Request):

        check_balance(req, self)
        check_send(req, self)

        req.end("", 401)


def create_node(node: Node) -> Node:

    path = input("Storage path (node/): ")
    if not path:
        path = "node_storage"

    node.set_storage(path)

    cert = input("Path to SSL certificate (keys/fullchain.pem): ")
    if not cert:
        cert = "keys/fullchain.pem"

    key = input("Path to SLL private key (keys/privkey.pem): ")
    if not key:
        key = "keys/privkey.pem"

    port = input("Node port (" + str(Const.port) + "): ")
    if not port:
        port = Const.port
    port = int(port)

    node.start(cert, key, port)

    print("Node started!")
    print("Command line:")


if __name__ == "__main__":
    node = Node()
    create_node(node)

    while True:
        try:
            command = input("/").split(" ")

            if command[0] in ["issue", "mint"]:
                try:
                    node.issue(command[1], float(command[2]))
                except:
                    node.issue(command[2], float(command[1]))

            nodes_command(command, node.nodes)
        except:
            pass
