from tools.com.alpha import Flow, Path


def test_flow():
    p = Path("TEST", "layer", ["TASK", "SUB"])
    f = Flow(content="abc123", path=p, format="text", a=1, b=7, c="aaaa")

    s = str(p).encode() + b"""
text
a: 1
b: 7
c: aaaa

abc123"""

    assert f.to_bytes()[5:] == s
