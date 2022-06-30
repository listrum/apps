import json
from methods.send import Send
from node import Node, create_node, check_command
import os


class History(Node):
    def on_send(self, data: Send) -> None:
        try:
            with open(self.history_path + data.key) as f:
                history = f.readlines()
        except:
            history = []

        history.append(json.dumps(data.data) + "\n")

        if len(history) > 2:
            history.pop(0)

        print(self.history_path)
        with open(self.history_path + data.key, "w") as f:
            f.writelines(history)

    def history(self, path: str = "history") -> None:
        if path[-1:] != "/":
            path += "/"

        try:
            os.makedirs(path)
        except:
            pass

        self.history_path = path

    def new_method(self, method: str, body):
        if method == "history":
            try:
                with open(self.history_path + body) as f:
                    return f.readlines()

            except:
                return []


if __name__ == "__main__":
    node = History()

    path = input("History path: ")
    if not path:
        path = "history"

    node.history(path)
    create_node(node)

    while True:
        command = input("/").split(" ")
        check_command(node, command)

        if command[0] == "history":
            node.history(command[1])
