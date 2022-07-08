from utils.https import Request, Server
from components.nodes import Nodes, nodes_command
from components.error import Error


class KeyStorage(Server):

    def __init__(self, wallet: str, path: str = "key_storage") -> None:
        if path[-1:] != "/":
            path += "/"

        self.path = path
        self.nodes = Nodes()
        self.wallet = wallet

        self.price = 1.0

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

    def add_key(self, username: str, key: str) -> None:
        with open(self.path + username, "x") as f:
            f.write(key)

    def check_value(self, from_priv: dict) -> None:
        value = self.nodes.client(from_priv)
        temp_wallet = self.nodes.client()

        if value.balance() < self.price:
            Error("Bad price")

        value.send(temp_wallet.owner, self.price)

        if temp_wallet.balance() < self.price:
            Error("Unable to trasfer")

        temp_wallet.send(self.wallet, self.price)


if __name__ == "__main__":
    app = KeyStorage()

    path = input("Key storage path: ")
    if not path:
        path = "key_storage"

    app.path = path

    while True:
        command = input("/").split(" ")

        nodes_command(command, app.nodes)
