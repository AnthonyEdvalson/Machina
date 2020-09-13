from tools.config.configloader import ConfigLoader
from vertex.vertex.logic import Logic
from vertex.vertex.vertexserver import VertexServer


def main():
    config = ConfigLoader("PATH", "MODE").load_json()
    logic = Logic(config)

    server = VertexServer(config, logic)
    print(server.port)
    server.serve()


main()
