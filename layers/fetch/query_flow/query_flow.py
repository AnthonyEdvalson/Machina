from abc import ABC
from query_flow.meta import Meta


class QueryFlow(ABC):
    def __init__(self, meta):
        self.meta = Meta() if meta is None else meta

    # Wrapper for all the meta timers

    def start_flow(self):
        self.meta.total_span.start_timer()

    def end_flow(self):
        self.meta.response_span.end_timer()

    def start_request(self):
        self.meta.request_span.start_timer()

    def end_request(self):
        self.meta.request_span.end_timer()

    def start_source(self):
        self.meta.source_span.start_timer()

    def end_source(self):
        self.meta.source_span.end_timer()

    def start_response(self):
        self.meta.request_span.start_timer()

    def end_response(self):
        self.meta.request_span.end_timer()
