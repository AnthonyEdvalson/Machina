class OverQuotaError(Exception):
    def __init__(self):
        super().__init__("Over Quota")


class TooManyRetriesError(Exception):
    def __init__(self):
        super().__init__("Too many retries")


class NotAuthenticatedError(Exception):
    def __init__(self):
        super().__init__("Not Authenticated")


class SourceError(Exception):
    def __init__(self, response):
        super().__init__("Source Error: \n" + str(response))
