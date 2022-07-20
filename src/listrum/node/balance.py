from client.https import Request
from node.tx.storage import storage

def check_balance(req: Request) -> None:
    if req.method != "balance":
        return

    req.end(storage.get(req.body))
