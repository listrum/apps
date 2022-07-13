
from node_utils.repay import Repay
from node_utils.storage import Storage
from node_utils.tx_list import TxList

from utils.https import Server

from components.nodes import Nodes


class NodePrototype(Server):
    tx_list = TxList()
    nodes = Nodes()
    repay = Repay()
    primary = Nodes()

    config = {}

    storage = Storage(config["storage"], nodes)

    def issue(self, value: int) -> None:
        pass
