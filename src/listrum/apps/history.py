import json
import os

from listrum.node.tx import Tx
from listrum.client.https import Request

path = os.path.expanduser("~") + "/listrum/history/"

try:
    os.makedirs(path)
except:
    pass


def on_send_history(tx: Tx) -> None:

    try:
        with open(path + tx.wallet)as f:
            from_history = json.loads(f.read())
    except:
        from_history = []

    try:
        with open(path + tx.to)as f:
            to_history = json.loads(f.read())
    except:
        to_history = []

    from_history.append(tx.data)
    to_history.append(tx.data)

    if len(from_history) > 4:
        from_history.pop(0)

    if len(to_history) > 4:
        to_history.pop(0)

    with open(path + tx.to, "w")as f:
        f.write(json.dumps(to_history))

    with open(path + tx.wallet, "w")as f:
        f.write(json.dumps(from_history))


def on_history(req: Request) -> None:
    if req.method != "history":
        return

    try:
        with open(path + str(req.body))as f:
            req.end(f.read())
    except:
        req.end("[]")
