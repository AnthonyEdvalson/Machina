from abc import ABC, abstractmethod


class Limiter(ABC):
    def query_success(self, weight=1):
        pass

    def query_fail(self, weight=1):
        pass

    @abstractmethod
    def over_used(self):
        pass


class PercentLimiter(Limiter):
    @abstractmethod
    def percent_used(self):
        pass

    def over_used(self):
        return self.percent_used() >= 1
