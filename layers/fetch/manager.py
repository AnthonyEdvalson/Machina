from abc import ABC, abstractmethod
from enum import Enum

from errors import TooManyRetriesError


class FailAction(Enum):
    Cancel = 0
    Retry = 1


class Manager(ABC):
    def __init__(self, validator, queries):
        self.queries = queries
        self.validator = validator

    def send(self, query: str, data: dict):

        try:
            q = self.queries[query]
        except KeyError:
            raise KeyError("{} not found in queries, available options are {}".format(query, list(self.queries.keys())))

        tries = 1
        errors = []
        while True:
            if tries > 3:
                for e in errors:
                    print(str(e))

                raise TooManyRetriesError()

            try:
                raw_response = q(**data)
                self.validator.validate(raw_response)
                break

            except Exception as e:
                errors.append(e)
                action = self._handle_error(e)

                if action == FailAction.Cancel:
                    raise e

            tries += 1

        return self._parse(raw_response)

    def _handle_error(self, e):
        return FailAction.Cancel

    def _get_fetch_args(self, request):
        return []

    @abstractmethod
    def _parse(self, raw_response):
        pass
