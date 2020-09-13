import requests

from limiters.unlimited_limiter import UnlimitedLimiter
from managers.http_manager import HttpManager
from source import Source
from validator import Validator


class Source1(Source):
    def __init__(self, config):
        queries = {
            "Query1": self.query1,
            "Query2": self.query2
        }

        super().__init__("Source1", UnlimitedLimiter(), HttpManager(queries, self.Source1Validator()))

    @staticmethod
    def query1(data):
        return requests.get("https://jsonplaceholder.typicode.com/todos/1")

    @staticmethod
    def query2(data):
        return requests.get("https://jsonplaceholder.typicode.com/todos/2")

    class Source1Validator(Validator):
        def validate(self, raw_response):
            return True
