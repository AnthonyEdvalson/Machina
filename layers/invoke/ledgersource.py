from abc import ABC, abstractmethod


class LedgerSource(ABC):
    @abstractmethod
    def pull(self):
        pass
