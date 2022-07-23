
from listrum.node import Request
from listrum.client import Client, nodes


def on_connect(req: Request) -> None:
    if req.method != "connect":
        return

    cash = Client(req.body["cash"])
    cash.withdraw(1)

    nodes.add(req.body["node"])

    req.end()
