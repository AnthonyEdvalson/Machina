from tools.events.event import Event
from abc import ABC, abstractmethod


class Trigger(ABC):
    def __init__(self):
        self.on_trigger = Event()

    def subscribe(self, func):
        self.on_trigger.subscribe(func)

    def unsubscribe(self, func):
        self.on_trigger.unsubscribe(func)

    def _invoke(self, *args):
        self.on_trigger.invoke(*args)

    @abstractmethod
    def prime(self):
        pass

    @abstractmethod
    def close(self):
        pass
