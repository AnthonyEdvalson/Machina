from trigger import Trigger


class FunctionTrigger(Trigger):
    def __init__(self, preprime=True):
        super().__init__()
        self.locked = True

        if preprime:
            self.prime()

    def invoke(self, *args):
        if not self.locked:
            self._invoke(*args)
            print('TRIGGER: Trigger invoked by function call')
        else:
            print("TRIGGER: invoke attempted, but trigger has not been primed")

    def prime(self):
        self.locked = False

    def close(self):
        self.locked = True
