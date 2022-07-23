from listrum.client.https import Request
from listrum.client import Client
import os

path = os.path.expanduser("~") + "/listrum/key_storage/"

try:
    os.makedirs(path)
except:
    pass


def on_sotore(req: Request) -> None:
    if req.method != "store":
        return

    cash = Client(req.body["cash"])
    cash.withdraw(1)

    try:
        open(path + req.body["name"])
        req.end("", 400)
        return
    except:
        pass

    with open(path + req.body["name"], "w") as f:
        f.write(str(req.body["key"]))

    req.end()


def on_store_get(req: Request) -> None:

    if req.method != "get":
        return

    with open(path + str(req.body)) as f:
        req.end(f.read())
