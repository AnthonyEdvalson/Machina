from ledger import Ledger
from ledgersources.constantledgersource import ConstantLedgerSource
from queryset import QuerySet
from triggers.functiontrigger import FunctionTrigger
from query import Query
import pandas as pd


def test_queryset():

    lut = FunctionTrigger()

    ledger1 = pd.DataFrame({
        "Key1": ["A1", "B1"],
        "Key2": ["A2", "B2"]
    })

    ledger2 = pd.DataFrame({
        "Key1": ["A1", "D1", "E1"],
        "Key2": ["A2", "D2", "E2"]
    })

    cls1 = ConstantLedgerSource(ledger1)
    cls2 = ConstantLedgerSource(ledger2)

    led1 = Ledger(lut, cls1)
    led2 = Ledger(lut, cls2)

    lut.invoke()

    qs = QuerySet([led1, led2], pd.DataFrame({
        "Source": ["S0", "S0"],
        "Query":  ["Q0", "Q2"]
    }))

    result_iterator = qs.join(3)

    results = result_iterator.as_list()

    target = pd.DataFrame({
        "Key1": ["A1", "B1", "D1", "A1", "B1", "D1", "E1", "E1"],
        "Key2": ["A2", "B2", "D2", "A2", "B2", "D2", "E2", "E2"],
        "Source": ["S0"] * 8,
        "Query": ["Q0", "Q2"] * 4
    })

    c = 0
    for result in results:
        row = target.loc[[c]]
        query = Query(**row.to_dict(orient="index")[c])
        assert query == result

        c += 1
