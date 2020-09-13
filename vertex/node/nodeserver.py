from tools.com.server import SmartServer
from vertex.router import Router


class NodeServer(SmartServer):
    def __init__(self, router: Router, host: str="localhost", port=0):
        super().__init__(router, host, port)
        self.host_name = host
        self.router = router

    def add_layer(self, name: str) -> None:
        self.router.enable(name)

    def remove_layer(self, name: str) -> None:
        self.router.disable(name)
