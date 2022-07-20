from client.https import Request
from node.tx.storage import Storage


def check_balance(req: Request) -> None:
    if req.method != "balance":
        return

    req.end(Storage().get(req.body))
