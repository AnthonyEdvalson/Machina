import pytest

from errors import TooManyRetriesError
from fetch_listener import Fetch
from tools.config.configloader import ConfigLoader
from vertex.task import Task


def test_fetch():
    c = ConfigLoader("tests/config.json", "default").load_json()

    fetch = Fetch(c)
    res = fetch.fetch(Task("Fetch/Fetch/Source1/Query1", {"data": 1}))

    assert res['id'] == 1
    assert not res['completed']

    res = fetch.fetch(Task("Fetch/Fetch/Source1/Query2", {"data": 1}))

    assert res['id'] == 2
    assert not res['completed']

    with pytest.raises(TooManyRetriesError):
        res = fetch.fetch(Task("Fetch/Fetch/BrokenSource/Query1", {"data": 1}))
