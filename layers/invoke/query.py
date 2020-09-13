class Query:
    def __init__(self, Source, Query, **args):
        self.source = Source
        self.query = Query
        self.args = args

    def __eq__(self, other):
        if type(other) is not Query:
            return False

        return self.source == other.source and \
            self.query == other.query and \
            self.args == other.args

    def to_dict(self):
        return {
            "source": self.source,
            "query": self.query,
            "args": self.args
        }
