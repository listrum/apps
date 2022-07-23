
from listrum import config
from listrum.node import Request
from listrum.client import Client, nodes
from listrum.client.error import Error


def on_connect(req: Request) -> None:
    if req.method != "connect":
        return

    cash = Client(req.body["cash"])
    temp = Client()

    cash.send_all(temp.wallet)

    if temp.balance() < 1*config.fee:
        raise Error("Not enough")

    nodes.add(req.body["node"])
    temp.send_all(config.wallet)

    req.end()
