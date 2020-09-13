from ledgersource import LedgerSource


class ConstantLedgerSource(LedgerSource):
    def __init__(self, data):
        self.data = data

    def pull(self):
        return self.data.copy()


