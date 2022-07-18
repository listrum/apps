from base64 import urlsafe_b64encode
import json
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import time
from utils.crypto import bytes_to_int, import_pub
from components.nodes import Nodes


class Client:

    def __init__(self, priv: dict = {}) -> None:

        if not priv:
            self.priv = ECC.generate(curve='P-256')

        else:
            self.priv = ECC.construct(d=bytes_to_int(priv["d"]),
                                      curve=priv["crv"],
                                      point_x=bytes_to_int(priv["x"]),
                                      point_y=bytes_to_int(priv["y"]))

        self.pub, self.wallet = import_pub(self.priv)

        self.nodes = Nodes()

    def get_owner(self, data: str) -> dict:

        time_stamp = int(time.time()*1000)

        data = data + str(time_stamp)
        data = SHA256.new(data.encode())

        sign = DSS.new(self.priv, 'fips-186-3').sign(data)

        owner = {
            "pub": self.pub,
            "time": time_stamp,
            "sign": urlsafe_b64encode(sign).decode()
        }

        return owner

    def send_all(self, to: str) -> None:
        data = {
            "to": to,
            "value": self.balance()
        }

        owner = self.get_owner(json.dumps(data).replace(" ", ""))

        data = {
            "data": data,
            "from": owner
        }

        self.nodes.send(data)

    def balance(self) -> float:
        return self.nodes.balance(self.wallet)