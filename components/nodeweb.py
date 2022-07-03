import json
import requests
from requests import Response

from components.constants import Const


class NodeWeb:
    def __init__(self, address: str) -> None:

        if address.find(":") < 0:
            address += ":" + Const.port_str

        self.address = "https://" + address

    def balance(self, owner: str) -> float:
        res = requests.get(self.address + "/balance/" + owner)
        return float(res.text)

    def issue(self, body: str) -> Response:

        return requests.get(self.address + "/issue/" + json.dumps(body))

    def send(self, body: str) -> Response:
        return requests.get(self.address + "/send/" + json.dumps(body))

    def history(self, owner: str) -> Response:
        return requests.get(self.address + "/history/" + owner)
