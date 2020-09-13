from abc import ABC, abstractmethod


class Cursor(ABC):
    @abstractmethod
    def execute(self, sql: str) -> None:
        pass

    @abstractmethod
    def fetch(self, count: int=1):
        pass

    @abstractmethod
    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class Connection(ABC):

    @abstractmethod
    def _make_cursor(self) -> Cursor:
        pass

    def transact(self):
        return self._make_cursor()
