class Event:
    def __init__(self):
        self.subs = []

    def subscribe(self, func):
        self.subs.append(func)

    def unsubscribe(self, func):
        self.subs.remove(func)

    def invoke(self, *args):
        for func in self.subs:
            func(*args)
