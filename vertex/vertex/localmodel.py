from vertex.lease import Lease
from vertex.resources import Resources
from vertex.worker import Worker


class Target:
    def __init__(self, name: str, port: int):
        self.name = name
        self.port = port


class LocalModel:
    def __init__(self):
        self.workers = {}
        self.leases = {}

    def get_workers(self):
        return self.workers

    def get_worker(self, name):
        return self.workers[name]

    def get_lease(self, lease_id):
        for worker in self.workers.values():
            for lease in worker.leases:
                if lease_id == lease.uid:
                    return lease

        raise Exception("Unknown id {}".format(lease_id))

    def add_worker(self, worker: Worker) -> None:
        assert worker.name not in self.workers
        self.workers[worker.name] = worker

    def add_lease(self, lease: Lease) -> None:
        name = lease.lessee
        self.workers[name].leases.append(lease)

    def get_worker_available_resources(self, name) -> Resources:
        worker = self.workers[name]
        leases = worker.leases

        total = worker.resources
        for lease in leases:
            total -= lease.resources

        return total

    def get_workers_by_layer(self, layer):
        result = []

        for worker in self.workers.values():
            leases = worker.leases
            for lease in leases:
                if lease.layer == layer and lease.is_valid():
                    result.append(worker)
                    break

        return result



"""
class LocalModel:
    def __init__(self):
        self.resource_keys = ["RAM", "CPU", "GPU", "storage", "network"]
        self.nodes = pd.DataFrame({"name": self.resource_keys + ["ip", "port", "task"]})
        self.tasks = pd.DataFrame({"name": ["task"] + self.resource_keys})

    def register_scheduler_node(self, name):
        pass

    def register_node(self, name: str, resources: Resources, ip: str, port: int, task: [str]):
        self.nodes.loc[name] = resources.to_list() + [ip, port, task]

    def get_resources(self, name):
        return Resources(*self.nodes.loc[name][:len(self.resource_keys)])

    def remove(self, name):
        if self.tasks.loc[name] is not None:
            raise Exception("Tasks still running")

        self.nodes.drop(name)
"""