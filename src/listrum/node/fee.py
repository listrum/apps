from listrum import config
from listrum.client.https import Request


def check_fee(req: Request) -> None:
    if req.method != "fee":
        return

    req.end(config.fee)
