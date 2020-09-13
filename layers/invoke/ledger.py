from tools.threads.readwritelock import ReadWriteLock


class Ledger:
    def __init__(self, update_trigger, ledger_source):
        self.ledger_source = ledger_source
        self.update_trigger = update_trigger
        self.cache = {}

        self.update_trigger.subscribe(self.update)
        self.update_trigger.prime()

        self.cache_lock = ReadWriteLock()

    def update(self):

        data = self.ledger_source.pull()

        self.cache_lock.acquire_write()
        self.cache = data
        self.cache_lock.release_write()

    def get(self):

        self.cache_lock.acquire_read()
        data = self.cache
        self.cache_lock.release_read()

        return data
