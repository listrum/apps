from base64 import urlsafe_b64encode
import json
from random import randint
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import time
from components.constants import Const
from components.nodes import NodeReq, Nodes, nodes_command
from utils.crypto import bytes_to_int, int_to_bytes, pad_key
from requests import Response
import getpass


class Client:

    def __init__(self, key: str = "") -> None:
        if not key:
            self.priv = ECC.generate(curve='P-256')

            self.owner = self.priv.public_key().export_key(format="DER")
            self.owner = urlsafe_b64encode(self.owner).decode()

        else:
            key = key.split("#")

            priv = json.loads(key[1])
            self.priv = ECC.construct(d=bytes_to_int(priv["d"]),
                                      curve=priv["crv"],
                                      point_x=bytes_to_int(priv["x"]),
                                      point_y=bytes_to_int(priv["y"]))

            self.owner = key[0]

        self.nodes = Nodes()
        self.key = pad_key(self.owner)

    def export_priv(self) -> str:
        return self.owner + "#" + json.dumps({
            "crv": self.priv.curve,
            "d": int_to_bytes(self.priv.d).replace("=", ""),
            "x": int_to_bytes(self.priv.pointQ.x).replace("=", ""),
            "y": int_to_bytes(self.priv.pointQ.y).replace("=", ""),
            "ext": True,
            "key_ops": ["sign"],
            "kty": "EC",
        })

    def get_owner(self, data: str) -> dict:

        time_stamp = int(time.time()*1000)

        data = data + str(time_stamp)
        data = SHA256.new(data.encode())

        sign = DSS.new(self.priv, 'fips-186-3').sign(data)

        owner = {
            "owner": self.owner,
            "time": time_stamp,
            "sign": urlsafe_b64encode(sign).decode()
        }

        return owner

    def send(self, to: str, value: float) -> Response:

        data = {
            "to": to,
            "value": float(value)/Const.fee
        }

        owner = self.get_owner(json.dumps(data).replace(" ", ""))

        data = {
            "data": data,
            "from": owner
        }

        self.nodes.send(data)


def check_command(cli: Client, command: list) -> None:

    if command[0] == "send":
        if len(str(command[1])) == Const.pad_length:
            cli.send(command[1], command[2])
        else:
            cli.send(command[2], command[1])

        print(cli.nodes.balance(cli.key))

    if command[0] in ["address", "key", "wallet", "balance"]:
        print(cli.key)
        print(cli.nodes.balance(cli.key))

    if command[0] in ["privkey", "private", "priv", "export"]:
        print(cli.export_priv())

    if command[0] in ["history", "tx"]:
        if len(command) < 2:
            res = cli.nodes[0].history(cli.key)
        else:
            res = NodeReq(command[1]).history(cli.key)

        for tx in json.loads(res.text):
            print(tx)


if __name__ == "__main__":

    cli = Client(getpass.getpass('Private key (optional): '))

    node = input("Node: ")
    if node:
        cli.nodes.add_node(node)

    while True:
        command = input("/").split(" ")
        check_command(cli, command)
        nodes_command(command, cli.nodes)
