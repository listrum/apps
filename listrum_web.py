import os
from https import Server


class ListrumWeb(Server):

    def __init__(self, port: int, certfile: str, keyfile: str) -> None:
        self.start_server(port, certfile, keyfile)

    def on_data(self, method: str, body: str):
        if method:
            return open("listrum_web/"+method).read()
        else:
            return open("listrum_web/index.html").read()
