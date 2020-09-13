import pandas as pa

from queryiterator import QueryIterator


class QuerySet:
    def __init__(self, ledgers, template):
        self.ledgers = ledgers
        self.template = template

    def join(self, block=64):
        all_leads = [l.get() for l in self.ledgers]
        leads = pa.concat(all_leads).drop_duplicates()

        leads.reset_index(drop=True, inplace=True)

        return QueryIterator(leads, self.template, block)
