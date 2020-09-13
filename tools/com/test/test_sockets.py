import os
import threading

import pytest

from tools.com.alpha import Path
from tools.com.client import SocketClient, ServerException
from tools.com.server import SocketServer


def test_sockets():
    val = None

    def recv(req):
        nonlocal val
        task = req.path.action_path[0]
        if task == "NULL":
            return None

        val = req.content["val"]
        return val + 1 if task == "ADD" else val - 1

    server = SocketServer(recv)
    run_server(server)   # start server in another thread

    with SocketClient("localhost", server.port) as client:

        assert val is None

        res = client.send_message(Path("TEST", "layer", "ADD"), {"val": 42}).content

        assert val == 42
        assert res == 43

        res = client.send_message(Path("TEST", "layer", "SUB"), {"val": 22}).content

        assert val == 22
        assert res == 21

        # This test is to ensure that null values can be transferred nicely
        res = client.send_message(Path("TEST", "layer", "NULL"), None).content

        assert val is 22
        assert res is None


def test_sockets_load():
    val = None

    def recv(data):
        nonlocal val
        val = data.content
        return bytes(reversed(data.content))

    data = os.urandom(256000)  # send ~256KB of random data
    reverse = bytes(reversed(data))

    server = SocketServer(recv, format="bytes")
    run_server(server)  # start server in another thread

    with SocketClient("localhost", server.port) as client:
        assert val is None

        res = client.send_message(Path("TEST", "layer", "test"), data, "bytes").content

        assert val == data
        assert res == reverse


def test_sockets_error():

    def server_error(req):
        print(req.content)
        raise Exception("There was a problem")

    server = SocketServer(server_error, format="json")
    run_server(server)  # start server in another thread

    client = SocketClient("localhost", server.port)
    client.connect()
    with pytest.raises(ServerException):
        client.send_message(Path("TEST", "layer", "test"), {"example": "data"}, "json")
    client.close()


def run_server(server):
    threading.Thread(target=server.serve).start()
