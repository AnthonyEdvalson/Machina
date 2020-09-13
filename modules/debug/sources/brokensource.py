from limiters.unlimited_limiter import UnlimitedLimiter
from managers.http_manager import HttpManager
from source import Source
from validator import Validator


class BrokenSource(Source):
    def __init__(self, config):
        queries = {
            "Query1": self.query1
        }

        super().__init__("BrokenSource", UnlimitedLimiter(), HttpManager(queries, self.BrokenValidator()))

    @staticmethod
    def query1(data):
        raise Exception("oops :(")

    class BrokenValidator(Validator):
        def validate(self, raw_response):
            return True
