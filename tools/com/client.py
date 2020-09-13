import socket
from sys import exc_info

from tools.com.alpha import Flow, Path


class SocketClient:
    def __init__(self, host: str, port: int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (host, port)

    def send_message(self, path: Path, data: any, format: str="json") -> Flow:
        req = Flow(content=data, path=path, format=format)

        try:
            print("CLIENT: Sending to {}:{} {}: {}".format(self.server_address[0], self.server_address[1], path, self.shorten(data)))
            self.socket.sendall(req.to_bytes())
        except BrokenPipeError:
            raise BrokenPipeError('BrokenPipeError: No connection').with_traceback(exc_info()[2])

        res = Flow.from_socket(self.socket)

        print("CLIENT: Received from {}:{} {}: {}".format(self.server_address[0], self.server_address[1], res.headers["Status"], self.shorten(res.raw)))

        if res.headers["Status"] == "ERROR":
            raise ServerException(res.content, path)

        return res

    def connect(self) -> None:
        print('CLIENT: connecting to %s port %s' % self.server_address)
        self.socket.connect(self.server_address)

    def close(self) -> None:
        print('CLIENT: closing socket')
        self.socket.close()

    def send_single(self, path: Path, data: any, format: str="json") -> Flow:
        self.connect()
        res = self.send_message(path, data, format)
        self.close()
        return res

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def shorten(self, msg: str, max_len: int=100) -> str:
        msg = str(msg)
        return msg if len(msg) < max_len else msg[:max_len] + '...'


class ServerException(Exception):
    def __init__(self, message: str, path: Path):
        super().__init__()
        self.message = message
        self.path = path

    def __str__(self):
        line = "\n\n" + "=" * 60 + "\n\n"
        return "Server Exception:" + line + self.message + line + str(self.path)
