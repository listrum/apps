from client.constants import Const
from client.https import Request


def check_fee(req: Request) -> None:
    if req.method != "fee":
        return

    req.end(Const.fee)
