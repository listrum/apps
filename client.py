from base64 import urlsafe_b64encode
import json
import math
from random import randint
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import time
from components.nodeweb import NodeWeb
from components.errors import Error
from utils.crypto import pad_key
from requests import Response


class Client:

    def __init__(self, key: str = "") -> None:
        if not key:
            self.priv = ECC.generate(curve='P-256')
        else:
            self.priv = ECC.import_key(key)

        self.nodes = []
        self.owner = urlsafe_b64encode(
            self.priv.public_key().export_key(format="DER")).decode()
        self.key = pad_key(self.owner)

    def export_priv(self) -> str:
        return self.priv.export_key(format="PEM")

    def get_owner(self, data: str) -> dict:

        time_stamp = int(time.time()*1000)

        data = data + str(time_stamp)

        # print(data)

        data = SHA256.new(data.encode())
        sign = DSS.new(self.priv, 'fips-186-3').sign(data)

        owner = {
            "owner": self.owner,
            "time": time_stamp,
            "sign": urlsafe_b64encode(sign).decode()
        }

        return owner

    def add_node(self, nodes: list) -> Response:
        for address in nodes:
            self.nodes.append(NodeWeb(address))

    def send(self, to: str, value: int) -> Response:

        to = {
            "to": to,
            "value": value
        }

        owner = self.get_owner(json.dumps(to).replace(" ", ""))

        data = {
            "to": to,
            "from": owner
        }

        rand_node = randint(0, len(self.nodes)-1)
        # print(data)
        return self.nodes[rand_node].send(data)

    def issue(self, value: int) -> Response:
        owner = self.get_owner(str(value))

        data = {
            "value": value,
            "from": owner
        }

        rand_node = randint(0, len(self.nodes)-1)
        return self.nodes[rand_node].issue(data)

    def balance(self) -> int:
        min = 9007199254740991
        res = 0

        for node in self.nodes:
            res = node.balance(self.key)

            if res < min:
                min = res

        if min == 9007199254740991:
            Error("No nodes")

        return min
