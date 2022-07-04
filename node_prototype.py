from components.repay import Repay
from components.constants import Const
from utils.https import Request, Server

from components.node_req import NodeReq
from components.tx_list import TxList
from components.storage import Storage


class NodePrototype(Server):

    def __init__(self) -> None:
        self.tx_list = TxList()
        self.nodes = []
        self.owner = ""

        self.repay = Repay()

    def start(self, certfile: str, keyfile: str, port: int = Const.port) -> None:
        self.start_server(port, certfile,
                          keyfile)

    def set_storage(self, node: str = "", dir: str = "node") -> None:
        self.storage = Storage(dir)

        if node:
            self.nodes.append(NodeReq(node))
            self.storage.set_node(node)

    def add_node(self, address: str) -> None:
        self.nodes.append(NodeReq(address))

    def remove_node(self, address: str) -> None:
        nodes = self.nodes

        for node in nodes:
            if node.address.find(address) >= 0:
                self.nodes.remove(node)

    def on_data(self, req: Request):
        pass
