import json

from errors import *
from validator import Validator


class SimilarValidator(Validator):
    def validate(self, raw_response):
        if raw_response == "invalid API key":
            raise NotAuthenticatedError()

        json_response = json.loads(raw_response)

        if json_response["meta"]["status"] != "Success":
            raise SourceError(raw_response)
