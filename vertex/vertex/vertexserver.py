from tools.com.server import SmartServer
from tools.config.config import Config
from vertex.resources import Resources
from vertex.router import Router
from vertex.task import Task
from vertex.vertex.logic import Logic


class VertexServer(SmartServer):
    def __init__(self, config: Config, logic: Logic, host: str="localhost", port=0):

        router = Router("Vertex", {"Connect": self.connect_node,
                                   "Lookup": self.lookup,
                                   "Disconnect": self.disconnect})

        layer_router = Router("VERTEX", {})
        layer_router.adopt(router)

        super().__init__(layer_router, host, port)

        self.config = config
        self.logic = logic

    def connect_node(self, task: Task):
        data = task.data
        resources = Resources(**data["resources"])
        name = data["name"]
        server_port = data["server_port"]

        self.logic.add_node(name, server_port, resources)
        leases = self.logic.allocate_worker(name)

        return {"config": self.config, "leases": leases}

    def disconnect(self, task: Task):
        raise NotImplemented()

    def lookup(self, task: Task):
        data = task.data
        task_to_find = data["layer"]

        target_worker = self.logic.call(task_to_find)

        return target_worker
