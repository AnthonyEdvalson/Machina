from abc import ABC, abstractmethod

from vertex.router import Router


def route(f):
    def wrap(*args, **kw):
        return f(*args, **kw)
    return wrap


class Layer(ABC):

    @abstractmethod
    def get_router(self) -> Router:
        pass
