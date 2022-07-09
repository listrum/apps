from urllib.request import Request
from listrum.components.constants import Const
from listrum.components.error import Error
from listrum.components.nodes import nodes_command
from listrum.node import create_node
from node.node_prototype import NodePrototype
from node.methods import check_balance, check_send


class Node(NodePrototype):

    def on_data(self, req: Request):

        check_balance(req, self)
        check_send(req, self)
        check_add(req, self)

        req.end("", 401)

    def set_wallet(self, wallet: str) -> None:
        self.wallet = wallet


def check_add(req: Request, self: Node) -> None:
    if req.method != "connect":
        return

    value = self.nodes.client(req.data["from"])
    temp_wallet = self.nodes.client()

    value.send_all(temp_wallet.wallet)

    if temp_wallet.balance() < 1/Const.fee*Const.fee*Const.fee:
        raise Error("Bad price")

    temp_wallet.send_all(self.wallet)

    self.nodes.add_node(req.data["data"])

    req.end()


if __name__ == "__main__":
    node = Node()

    wallet = input("Wallet: ")

    node.set_wallet(wallet)
    create_node(node)

    while True:
        command = input("/").split(" ")

        try:
            nodes_command(command, node.nodes)

            if command[0] in ["issue", "mint"]:
                try:
                    node.issue(command[1], float(command[2]))
                except:
                    node.issue(command[2], float(command[1]))

            if command[0] == "walllet":
                node.set_wallet(command[1])
        except:
            pass
