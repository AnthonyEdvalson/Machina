from requests import Session

from errors import *
from manager import Manager, FailAction
from tools.com import formatting


class HttpManager(Manager):
    def __init__(self, queries, validator, accept="json"):
        super().__init__(validator, queries)

        self.format = accept

        if accept == "json":
            full_accept = "application/json"
        else:
            raise Exception("Unknown format {}".format(accept))

        self.session = Session()
        self.session.headers.update({"Accept": full_accept})

    def _get_fetch_args(self, request):
        return [self.session]

    def _handle_error(self, e):
        if e is SourceError:
            return FailAction.Cancel

        if e is NotAuthenticatedError:
            return FailAction.Retry

    def _parse(self, raw_response):
        return formatting.deserialize(raw_response.content, self.format)
