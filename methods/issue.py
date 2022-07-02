
import time
from components.constants import Const
from node_prototype import NodePrototype
from components.storage import Storage
from components.errors import Error
from utils.https import Request
from utils.crypto import verify, pad_key


def check_issue(req: Request, node: NodePrototype) -> None:
    if req.method != "issue":
        return

    issue = Issue(req.body)

    issue.verify()

    issue.check_time()
    issue.check_owner(node.owner)

    node.tx_list.add(issue)
    issue.add(node.storage)

    for node in node.nodes:
        node.issue(req.body)

    req.end()


class Issue:
    def __init__(self, params: dict) -> None:
        self.owner = params["from"]["owner"]

        self.key = pad_key(self.owner)

        self.time = int(params["from"]["time"])

        self.sign = params["from"]["sign"]
        self.value = int(params["value"])

    def verify(self) -> None:
        verify(self.owner, str(self.value) +
               str(self.time), self.sign)

    def check_time(self) -> None:
        if abs(time.time()*1000 - self.time) > Const.tx_ttl:
            raise Error("Outdated")

    def check_owner(self, owner: str) -> None:
        if owner != self.key:
            raise Error("NotOwner")

    def add(self, storage: Storage) -> None:
        storage.set(self.key, storage.get(self.key) + self.value)
