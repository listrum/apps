import time

from listrum.client.constants import Const


class Repay:
    def __init__(self) -> None:
        self.total = 0
        self.current = 0
        self.before = 0

        self.last_update = time.time()*1000

    def add(self, amount: float) -> None:
        self.current += amount

        if time.time()*1000 - self.last_update > Const.repay_update:
            self.last_update = time.time()*1000
            self.total += self.before - self.current

            self.before = self.current
            self.current = 0

        if self.total > 0:
            res = self.total*Const.repay_value
            self.total -= res
        else:
            res = 0

        return res
