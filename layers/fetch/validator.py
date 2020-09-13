from abc import ABC, abstractmethod


class Validator(ABC):
    def pre_validate(self, request):
        pass

    @abstractmethod
    def validate(self, raw_response):
        pass
