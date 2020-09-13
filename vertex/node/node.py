from enum import Enum
from threading import Timer

from tools.com.alpha import Path
from tools.com.client import SocketClient
from tools.config.config import Config
from vertex.lease import Lease, LeaseState
from vertex.node.nodeserver import NodeServer
from vertex.resources import Resources


class NodeState(Enum):
    DISCONNECTED = 0  # node has no connection to vertex
    CONNECTED = 1  # node has connection to vertex, but is not running
    RUNNING = 2  # node is connected to vertex, and can take requests
    CLOSED = 3  # node is being shut down


class Node:
    def __init__(self, node_config: Config, server: NodeServer):
        self.boot_config = node_config

        self.state = NodeState.DISCONNECTED
        self.name = server.host_name
        self.vertex_host = self.boot_config["vertex_host"]
        self.vertex_port = self.boot_config["vertex_port"]
        self.resources = Resources(**self.boot_config["resources"])

        self.config = None
        self.node_config = None
        self.pending_leases = []
        self.leases = []

        self.server = server

    def clean(self):
        if self.state == NodeState.CLOSED:
            return

        Timer(self.node_config["clean_rate"], self.clean).start()

        self._allocate_leases()

        i = len(self.leases)
        while i > 0:
            i -= 1
            lease = self.leases[i]
            if not lease.is_valid():
                self.leases.remove(lease)

    def start(self):
        self.server.serve_async()

        with SocketClient(self.vertex_host, self.vertex_port) as client:
            msg = {"name": self.name, "server_port": self.server.port, "resources": self.resources}
            res = client.send_message(Path(self.vertex_host, "Vertex", "Connect"), msg)

            self.config = Config(res.content["config"])
            self.node_config = self.config.select("node")
            self.pending_leases = list(map(lambda l: Lease(**l), res.content["leases"]))

        self.state = NodeState.CONNECTED
        self.clean()

    def _allocate_leases(self):
        while len(self.pending_leases) > 0:
            lease = self.pending_leases[0]

            assert lease.state == LeaseState.SIGNED

            try:
                lease.activate()
                self.server.add_layer(lease.layer)
            except AssertionError:
                self.pending_leases.pop(0)  # remove lease with unknown name

                msg = "Unknown layer '{}', available options are {}\n".format(lease.layer, list(self.server.router.keys()))
                msg += "If this list of options is incorrect, correct the NodeServer's route"

                raise AssertionError(msg)

            self.pending_leases.pop(0)
            self.leases.append(lease)

    def call(self):
        pass

    def disconnect(self):
        with SocketClient(self.vertex_host, self.vertex_port) as client:
            res = client.send_message(Path(self.vertex_host, "Vertex", "Disconnect"), {"name": self.name})
            raise NotImplemented()

        self.state = NodeState.DISCONNECTED

    def close(self):
        # TODO decide if leases should be removed when closed
        self.state = NodeState.CLOSED
        self.server.close()
