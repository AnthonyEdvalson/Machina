from ledger import Ledger
from ledgersources.constantledgersource import ConstantLedgerSource
import numpy as np

from triggers.functiontrigger import FunctionTrigger


def test_ledger():
    arr = np.array([["id 1a", "id 1b"], ["id 2a", "id 2b"]])
    ls = ConstantLedgerSource(arr)
    t = FunctionTrigger()

    ledger = Ledger(t, ls)
    t.invoke()

    assert np.array_equal(ledger.get(), arr)

    arr.put([2, 3], ["id 3a", "id 3b"])

    assert not np.array_equal(ledger.get(), arr)

    t.invoke()

    assert np.array_equal(ledger.get(), arr)
