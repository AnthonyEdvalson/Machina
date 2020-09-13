import pytest

from tools.com.alpha import Path
from tools.com.client import SocketClient, ServerException
from tools.config.configloader import ConfigLoader
from vertex.lease import LeaseState
from vertex.node.node import Node
from vertex.node.nodeserver import NodeServer
from vertex.resources import Resources
from vertex.router import Router
from vertex.task import Task
from vertex.vertex.logic import Logic
from vertex.vertex.vertexserver import VertexServer


def gen_resources(ram_gb=16, cpu_cores=4, gpu_cores=0, storage_gb=150, network_mbs=100):

    return Resources(ram_gb=ram_gb, cpu_cores=cpu_cores, gpu_cores=gpu_cores,
                     storage_gb=storage_gb, network_mbs=network_mbs)


def test_vertex_general():
    config = ConfigLoader("tests/config.json", "default").load_json()
    boot_config = ConfigLoader("tests/node_config.json", "default").load_json()

    val = 0

    def task1(task: Task):
        nonlocal val
        val = task.data
        return val["x"] + 1

    with VertexServer(config, Logic(config)) as server:

        boot_config.alter("vertex_port", server.port)

        with pytest.raises(ServerException):
            SocketClient("localhost", server.port).send_single(Path("TEST", "Vertex", "Lookup"), {"layer": "layer1"})

        # connect and set up a new node
        layer_router = Router("Layer 1", {"task1": task1})
        node_router = Router("NODE", {"layer1": layer_router})
        node = Node(boot_config, NodeServer(node_router))
        node.start()

        assert node.config == config

        # activate lease for layer-1
        server.logic.activate_lease(server.logic.get_worker("localhost").leases[0].uid)
        assert node.leases[0].state == LeaseState.ACTIVE
        assert node.leases[0].is_valid()

        # start a new connection from a caller
        res = SocketClient("localhost", server.port).send_single(Path("TEST", "Vertex", "Lookup"), {"layer": "layer1"})
        print(res.raw)

        target = res.content["name"], res.content["server_port"]

        res = SocketClient(target[0], target[1]).send_single(Path(target[0], "layer1", "task1"), {"x": 44})

        assert val == {"x": 44}
        assert res.content == 45

        node.close()
