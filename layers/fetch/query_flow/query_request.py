from query_flow.query_flow import QueryFlow


class QueryRequest(QueryFlow):
    def __init__(self, source, query, args, meta=None):
        super().__init__(meta)
        self.source = source
        self.query = query
        self.args = args
