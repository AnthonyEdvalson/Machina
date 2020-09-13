from query_flow.query_flow import QueryFlow


class QueryResponse(QueryFlow):
    def __init__(self, request, data, errors=None):
        super().__init__(request.meta)
        self.data = data
        self.errors = errors if errors is list else [errors]
