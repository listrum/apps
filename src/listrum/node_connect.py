from utils.https import Request
from components.constants import Const
from components.error import Error
from components.nodes import nodes_command, Nodes
from node import create_node
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

    def primary_node(self, address: str) -> None:
        self.primary = Nodes()
        self.primary.add_node(address)


def check_add(req: Request, self: Node) -> None:
    if req.method != "connect":
        return

    value = self.primary.client(req.body["from"])
    temp_wallet = self.primary.client()

    value.send_all(temp_wallet.wallet)

    print(temp_wallet.balance(), 1.0/Const.fee*Const.fee*Const.fee)

    if temp_wallet.balance() < 1.0/Const.fee*Const.fee*Const.fee:
        raise Error("Bad price")

    temp_wallet.send_all(self.wallet)

    self.nodes.add_node(req.body["data"])

    req.end()


if __name__ == "__main__":
    node = Node()
    node.set_wallet(input("Wallet: "))
    node.primary_node(input("Primary node: "))
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
