from listrum.node import Node, Request
from listrum.apps.history import on_send_history, on_history
from listrum.apps.node_connect import on_connect
from listrum.apps.key_storage import on_sotore, on_store_get


def on_request(req: Request) -> None:
    on_history(req)
    on_connect(req)

    on_sotore(req)
    on_store_get(req)


node = Node()
node.on_send = on_send_history
node.on_request = on_request
