from errors import *
from limiter import Limiter
from manager import Manager


class Source:
    def __init__(self, name: str, limiter: Limiter, manager: Manager):
        self.name = name
        self.limiter = limiter
        self.manager = manager

    # wrappers
    def over_used(self) -> bool:
        return self.limiter.over_used()

    def fetch(self, query: str, data: dict) -> None:
        if self.over_used():
            raise OverQuotaError()

        return self.manager.send(query, data)
