import json

from components.constants import Const
from components.error import Error

from utils.https import Request
from utils.crypto import pad_key

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

    # print(send.to, send.wallet, send.value)

    send.verify()
    send.check_time()
    send.check_value(node.storage)
    send.repay(node)

    node.tx_list.add(send)

    send.add_value(node.storage)

    req.end()

    node.nodes.send(req.body)

    # print(send.to, send.value)

    # print(1)
