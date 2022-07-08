from base64 import urlsafe_b64encode
import json
from random import randint
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import time
from components.constants import Const
from utils.crypto import bytes_to_int, import_pub
from requests import Response


class Client:

    def __init__(self, key: dict = {}) -> None:

        if not key:
            self.priv = ECC.generate(curve='P-256')

        else:
            self.priv = ECC.construct(d=bytes_to_int(key["d"]),
                                      curve=key["crv"],
                                      point_x=bytes_to_int(key["x"]),
                                      point_y=bytes_to_int(key["y"]))

        self.key, self.owner = import_pub(self.priv)

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

    def balance(self) -> float:
        return self.nodes.balance(self.owner)

    def set_nodes(self, nodes) -> None:
        self.nodes = nodes
