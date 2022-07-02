from components.storage import Storage
from utils.https import Request


def check_balance(req: Request, node) -> None:
    if req.method != "balance":
        return

    req.end(node.storage.get(req.body))
