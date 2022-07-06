from components.repay import Repay
from components.constants import Const
from utils.https import Request, Server

from listrum.components.nodes import NodeReq, Nodes
from components.tx_list import TxList
from components.storage import Storage


class NodePrototype(Server):

    def __init__(self) -> None:
        self.tx_list = TxList()
        self.nodes = Nodes()

        self.repay = Repay()

    def start(self, certfile: str, keyfile: str, port: int = Const.port) -> None:
        self.start_server(port, certfile,
                          keyfile)

    def set_storage(self, node: str = "", dir: str = "node") -> None:
        self.storage = Storage(dir)

        if node:
            self.nodes.append(NodeReq(node))
            self.storage.set_node(node)

    def issue(self, address: str, value: float) -> None:
        self.storage.set(address, self.storage.get(address) + value)

    def on_data(self, req: Request):
        pass
