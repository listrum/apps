from utils.https import Request, Server
from components.nodes import Nodes, nodes_command


class KeyStorage(Server):

    def __init__(self) -> None:
        self.path = "key_storage"
        self.nodes = Nodes()

        self.price = 1.0

    def on_data(self, req: Request) -> None:

        if req.method == "store":
            self.store_key(self.body["data"], self.body["pay"])

    def store_key(self, data: dict, pay: dict) -> None:
        self.nodes.balance(pay["owner"])


if __name__ == "__main__":
    app = KeyStorage()

    path = input("Key storage path: ")
    if not path:
        path = "key_storage"

    app.path = path

    while True:
        command = input("/").split(" ")

        nodes_command(command, app.nodes)
