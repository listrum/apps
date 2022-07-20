import time
from listrum.client.constants import Const
from listrum.client.error import Error


class TxList:

    def __init__(self) -> None:
        self.tx_list = []

    def add(self, new_tx) -> None:

        for tx in self.tx_list:
            if tx.sign == new_tx.sign:
                raise Error("Already sent")

        self.tx_list.append(new_tx)

        if abs(self.tx_list[0].time - time.time()*1000) > Const.tx_ttl:
            self.tx_list.pop(0)
