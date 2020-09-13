import pandas as pd
from query import Query


class QueryIterator:
    def __init__(self, query_keys, queries, block=16):
        self.query_keys = query_keys
        self.queries = queries

        self._block_size = block

    def __iter__(self):
        self.idx = 0
        self._block = None
        return self

    def __next__(self):
        if len(self) <= self.idx:
            raise StopIteration

        query_count = len(self.queries)

        if self.idx % (self._block_size * query_count) == 0:
            self._block = self._get_block(self.idx, self._block_size)

        row = self._block.loc[[self.idx]]
        query = Query(**row.to_dict(orient="index")[self.idx])

        self.idx += 1
        return query

    def _get_block(self, start, size):
        query_count = len(self.queries)

        key_start = start // query_count
        act_size = min(size, len(self.query_keys) - key_start)

        k = pd.concat([self.query_keys.iloc[key_start:key_start + act_size]] * query_count)
        q = pd.concat([self.queries] * act_size)

        k.index = range(start, start + act_size * query_count)
        q.index = range(start, start + act_size * query_count)

        return pd.concat([k, q], axis=1)

    def __len__(self):
        return self.queries.shape[0] * self.query_keys.shape[0]

    def as_list(self):
        return [x for x in self]
