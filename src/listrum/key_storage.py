from asyncio import start_server
import json
from components.constants import Const
from utils.https import Request, Server
from components.nodes import Nodes, nodes_command
from components.error import Error
import os


class KeyStorage(Server):

    def __init__(self, wallet: str, path: str) -> None:
        if path[-1:] != "/":
            path += "/"

        try:
            os.mkdir(path)
        except:
            pass

        self.path = path
        self.nodes = Nodes()
        self.wallet = wallet

        self.price = 1.0

    def start(self, certfile: str, keyfile: str, port: int = Const.port) -> None:
        self.start_server(port, certfile,
                          keyfile)

    def on_data(self, req: Request) -> None:

        if req.method == "store":
            self.check_value(req.body["from"])
            self.add_key(req.body["data"]["username"], req.body["data"]["key"])
            req.end()

        if req.method == "get_key":
            req.end(self.get(req.body))

    def get(self, username: str) -> str:
        with open(self.path + username) as f:
            return f.read()

    def add_key(self, username: str, key: list) -> None:
        with open(self.path + username, "x") as f:
            f.write(json.dumps(key))

    def check_value(self, from_priv: dict) -> None:
        value = self.nodes.client(from_priv)
        temp_wallet = self.nodes.client()

        value.send_all(temp_wallet.key)

        if temp_wallet.balance() < self.price*Const.fee:
            Error("Bad price")

        temp_wallet.send_all(self.wallet)


if __name__ == "__main__":

    path = input("Key storage path: ")
    if not path:
        path = "key_storage"

    app = KeyStorage(input("Your wallet: "), path)

    cert = input("Path to SSL certificate (keys/fullchain.pem): ")
    if not cert:
        cert = "keys/fullchain.pem"

    key = input("Path to SLL private key (keys/privkey.pem): ")
    if not key:
        key = "keys/privkey.pem"

    port = input("Storage port (" + str(Const.storage_port) + "): ")
    if not port:
        port = Const.storage_port
    port = int(port)

    app.start(cert, key, port)

    while True:
        command = input("/").split(" ")

        nodes_command(command, app.nodes)

        if command[0] == "wallet":
            app.wallet = command[1]
