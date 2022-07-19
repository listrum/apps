
from components.constants import Const

from utils.https import Request

from node_utils.node_prototype import NodePrototype
from node_utils.send import Send


def check_fee(req: Request) -> None:
    if req.method != "fee":
        return
    req.end(Const.fee)


def check_balance(req: Request, node: NodePrototype) -> None:
    if req.method != "balance":
        return

    req.end(node.storage.get(req.body))


def check_send(req: Request, node: NodePrototype) -> None:
    if req.method != "send":
        return

    send = Send(req.body)

    send.verify()
    send.check_time()
    send.check_value(node.storage)
    send.repay(node)

    node.tx_list.add(send)

    send.add_value(node.storage)

    req.end()
    node.on_send(send)
    node.nodes.send(req.body)
