from limiters.unlimited_limiter import UnlimitedLimiter
from managers.http_manager import HttpManager
from source import Source
from validator import Validator


class Source2(Source):
    def __init__(self, config):
        queries = {
            "Query3": self.query1,
            "Query4": self.query2
        }

        super().__init__("Source2", UnlimitedLimiter(), HttpManager(queries, self.Source2Validator()))

    @staticmethod
    def query1(data):
        pass

    @staticmethod
    def query2(data):
        pass

    class Source2Validator(Validator):
        def validate(self, raw_response):
            return True
