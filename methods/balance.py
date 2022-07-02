from node_prototype import NodePrototype
from utils.https import Request


def check_balance(req: Request, node: NodePrototype) -> None:
    if req.method != "balance":
        return

    req.end(node.storage.get(req.body))
