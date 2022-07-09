from utils.https import Request, Server

from components.nodes import Nodes
from components.constants import Const

from node.tx_list import TxList
from node.storage import Storage
from node.repay import Repay


class NodePrototype(Server):

    def __init__(self) -> None:
        self.tx_list = TxList()
        self.nodes = Nodes()

        self.repay = Repay()

    def set_storage(self, dir: str = "node") -> None:
        self.storage = Storage(dir, self)

    def issue(self, wallet: str, value: float) -> None:
        self.storage.set(wallet, self.storage.get(wallet) + value)

    def on_data(self, req: Request):
        pass
