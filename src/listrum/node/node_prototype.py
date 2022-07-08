from listrum.node.repay import Repay
from components.constants import Const
from utils.https import Request, Server

from components.nodes import Nodes
from listrum.node.tx_list import TxList
from listrum.node.storage import Storage


class NodePrototype(Server):

    def __init__(self) -> None:
        self.tx_list = TxList()
        self.nodes = Nodes()

        self.repay = Repay()

    def start(self, certfile: str, keyfile: str, port: int = Const.port) -> None:
        self.start_server(port, certfile,
                          keyfile)

    def set_storage(self, dir: str = "node") -> None:
        self.storage = Storage(dir, self)

    def issue(self, wallet: str, value: float) -> None:
        self.storage.set(wallet, self.storage.get(wallet) + value)

    def on_data(self, req: Request):
        pass
