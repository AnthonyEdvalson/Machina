import socket
import threading
import traceback

from tools.com.alpha import Flow, Path
from vertex.router import Router
from vertex.task import Task


class SocketServer:
    def __init__(self, target, host: str="localhost", port: int=0, format: str="json", backlog: int=10):
        self.format = format
        self.target = target
        self.closing = False
        self.threads = []

        print("SERVER: Opening at {}:{}".format(host, port))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(backlog)
        s.settimeout(1)  # TODO remove when using select.poll
        self.socket = s
        self.port = s.getsockname()[1]

    def serve(self):
        while True:
            print("SERVER: Waiting for connections")
            while True:
                try:
                    conn, addr = self.socket.accept()
                    break
                except socket.timeout:
                    if self.closing:
                        for t in self.threads:
                            t.join()
                        print("SERVER: Closed")
                        return

            # TODO use select.poll to prevent creating multiple threads
            t = threading.Thread(target=self._handle_request, args=(conn, addr))
            t.start()

            self.threads = list(filter(lambda x: x.isAlive(), self.threads))
            self.threads.append(t)

    def serve_async(self):
        return threading.Thread(target=self.serve).start()

    def _handle_request(self, conn, addr):
        while True:
            try:
                req = Flow.from_socket(conn)

                if req is None:
                    break

                print("SERVER: Received from {}:{} {}".format(addr[0], addr[1], self.shorten(req.raw)))
                print("SERVER: handling on {}".format(threading.current_thread().name))

                res_data = self.target(req)
                status = "OKAY"
                res = Flow(content=res_data, path=req.path, format=self.format, Status=status)
            except Exception as e:
                status = "ERROR"
                res = Flow(content=traceback.format_exc() + "\n\n" + str(e), path=Path.empty(), format="text", Status=status)

            res_bytes = res.to_bytes()

            print("SERVER: Replying to {}:{} with {}: {}".format(addr[0], addr[1], status, self.shorten(res_bytes)))
            conn.sendall(res_bytes)

        conn.close()

    def shorten(self, msg, max_len=100):
        msg = str(msg)
        return msg if len(msg) < max_len else msg[:max_len] + '...'

    def close(self):
        print("SERVER: Closing, {} threads running...".format(len(self.threads)))
        self.closing = True

    def __enter__(self):
        self.serve_async()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class SmartServer(SocketServer):
    def __init__(self, router: Router, host="localhost", port=0, format="json", backlog=10):
        super().__init__(self._route_request, host, port, format, backlog)
        self.router = router

    def _route_request(self, req: Flow):
        task = Task.from_request(req)
        return self.router.route_and_call(task)
