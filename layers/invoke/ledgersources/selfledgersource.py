from ledgersource import LedgerSource


class SelfLedgerSource(LedgerSource):
    def __init__(self, name):
        self.url = "https://www.example.com/ledgers/{}".format(name)

    def pull(self):
        # TODO pull from Machina endpoint
        raise NotImplemented()
        pass
