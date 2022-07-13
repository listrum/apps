import json
from components.constants import Const
from utils.https import Request, Server
from components.nodes import Nodes, nodes_command
from components.error import Error
import os


class KeyStorage(Server):

    def __init__(self) -> None:

        with open("config.json") as f:
            self.config = json.loads(f.read())

        self.path = self.config["key_storage"]["path"]

        if self.path[-1:] != "/":
            self.path += "/"

        try:
            os.mkdir(self.path)
        except:
            pass

        self.nodes = Nodes()
        self.wallet = self.config["wallet"]

        self.price = self.config["key_storage"]["price"]

        self.start_server(
            self.config["key_storage"]["port"], self.config["cert"], self.config["cert_key"])

    def on_data(self, req: Request) -> None:

        if req.method == "store":
            self.check_value(req.body["from"])
            self.add_key(req.body["data"]["name"], req.body["data"]["key"])
            req.end()

        if req.method == "get":
            req.end(self.get(req.body))

        if req.method == "price":
            req.end(self.price)

        req.end("", 401)

    def get(self, name: str) -> str:
        with open(self.path + str(name)) as f:
            return f.read()

    def add_key(self, name: str, key: list) -> None:
        with open(self.path + name, "x") as f:
            f.write(json.dumps(key))

    def check_value(self, priv: dict) -> None:
        value = self.nodes.client(priv)
        temp_wallet = self.nodes.client()

        value.send_all(temp_wallet.wallet)

        if temp_wallet.balance() < self.price*Const.fee:
            raise Error("Bad price")

        temp_wallet.send_all(self.wallet)


if __name__ == "__main__":
    app = KeyStorage()

    node = input("Add node: ")
    app.nodes.add_node(node)

    print("Key storage started!")

    while True:
        command = input("/").split(" ")

        try:
            nodes_command(command, app.nodes)

        except:
            pass
