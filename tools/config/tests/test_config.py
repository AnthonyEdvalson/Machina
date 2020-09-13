import pytest

from tools.config.config import Config


def test_get():
    c = gen_conf()

    assert c["l1a"] == 123
    assert c["l1b"] == "abc"
    assert c["l1c"] == {"l2a": ["l3a", "l3b"], "l2b": 555, "l2c": {"l3a": 4}}

    with pytest.raises(KeyError):
        print(c["lxx"])
    with pytest.raises(KeyError):
        print(c["l2a"])
    with pytest.raises(KeyError):
        print(c["l1c/l2a/xxx"])

    assert c.get("lxx") is None
    assert c.get("l1c/lxx") is None
    assert c.get("l2a") is None
    assert c.get("lxx", 555) == 555


def test_select():
    c = gen_conf()

    assert c["l1c/l2a"] == c.select("l1c")["l2a"]
    assert c.select("l1c")["l2b"] == 555
    assert c.select("l1c/l2c")["l3a"] == 4

    with pytest.raises(KeyError):
        c.select("lxx")
    with pytest.raises(KeyError):
        c.select("l1c/lxx")


def test_alter():
    c = gen_conf()

    assert c.get("l1a") == 123
    c.alter("l1a", 111)
    assert c.get("l1a") == 111
    assert c.get("l1b") == "abc"

    c.select("l1c").alter("l2a", [])
    assert c.get("l1c/l2a") == []

    c.alter("l1c/l2a", [1])
    assert c.get("l1c/l2a") == [1]

    with pytest.raises(KeyError):
        c.alter("lxx", 999)
    with pytest.raises(KeyError):
        c.alter("l1c/lxx", 888)

    c.alter("lxx", 999, False)
    assert c.get("lxx") == 999

    c.alter("l1c/lxx", 888, False)
    assert c.get("l1c/lxx") == 888


def gen_conf():
    return Config({"l1a": 123, "l1b": "abc", "l1c": {"l2a": ["l3a", "l3b"], "l2b": 555, "l2c": {"l3a": 4}}})
