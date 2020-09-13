import time


class Meta:
    def __init__(self):
        self.total_span = Span()
        self.request_span = Span()
        self.source_span = Span()
        self.response_span = Span()


class Span:
    def __init__(self):
        self.start = None
        self.end = None

    def start_timer(self):
        self.start = time.time()

    def end_timer(self):
        self.end = time.time()

    def duration(self):
        assert self.start is not None
        assert self.end is not None
        return self.end - self.start
