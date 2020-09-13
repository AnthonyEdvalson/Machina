from tools.config.configloader import ConfigLoader
from vertex.node.node import Node
from vertex.node.nodeserver import NodeServer
from vertex.vertex.vertexserver import VertexServer


def test_node_general():
    return

    def route_a(req):
        return

    def route_b(req):
        return

    router = {"a": route_a, "b": route_b}

    boot_config = ConfigLoader("tests/node_config.json", "default").load_json()
    node = Node(boot_config, NodeServer(router, "localhost"))



    node.start()