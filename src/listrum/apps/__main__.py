import imp
from listrum.client.https import Request
from listrum.node import Node
from listrum.apps.history import on_send_history, on_history


def on_request(req: Request) -> None:
    on_history(req)


node = Node()
node.on_send = on_send_history
node.on_request = on_request
