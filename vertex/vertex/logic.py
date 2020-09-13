import random

from vertex.lease import Lease, LeaseState
from vertex.resources import Resources
from vertex.vertex.localmodel import LocalModel
from vertex.worker import Worker


class NoWorkers(Exception):
    def __init__(self, layer):
        super().__init__("No workers on layer '{}'".format(layer))


class Logic:
    def __init__(self, config):
        self.lease_queue = []
        self.model = LocalModel()
        self.config = config

        self.update_lease_queue()

    def get_workers(self) -> {str: Worker}:
        return self.model.get_workers()

    def get_worker(self, name):
        return self.model.get_worker(name)

    def add_node(self, name: str, server_port: int, resources: Resources) -> None:
        self.model.add_worker(Worker(name, server_port, resources))

    def activate_lease(self, lease_id: str):
        lease = self.model.get_lease(lease_id)
        assert lease.state == LeaseState.SIGNED
        lease.activate()

    def allocate_worker(self, name: str) -> [Lease]:
        new_leases = []

        available = self.model.get_worker_available_resources(name)

        for lease in self.lease_queue:
            if not available.can_contain(lease.resources):
                break

            self.lease_queue.remove(lease)

            lease.sign(name)

            self.model.add_lease(lease)
            new_leases.append(lease)
            continue

        return new_leases

    def get_layer_load(self, layer_name: str):
        raise NotImplemented()

    def get_all_loads(self):
        raise NotImplemented()

    def get_target_lease_count(self) -> {str: int}:
        target = {}

        # TODO implement an actual algorithm
        for layer in self.config["layers"]:
            target[layer] = 1

        return target

    def get_lease_layer_count(self) -> {str: int}:
        counts = {}

        for lease in self.lease_queue:
            if lease.layer not in counts:
                counts[lease.layer] = 1
            else:
                counts[lease.layer] += 1

        return counts

    def update_lease_queue(self, allocate=True):
        target = self.get_target_lease_count()
        counts = self.get_lease_layer_count()

        deltas = {}

        for k, v in target.items():
            if k in counts:
                deltas[k] = v - counts[k]
            else:
                deltas[k] = v

        for layer, delta in deltas.items():
            resources = Resources(**self.config["layers"][layer]["resources"])
            for i in range(0, delta):
                self.lease_queue.append(Lease(layer, resources))

        if allocate:
            for worker in self.model.get_workers():
                self.allocate_worker(worker)

    """
        Returns a worker that is able to do work on a specific layer. If no workers are able to act on that layer
        at the moment, None is returned. If no workers are on that layer, something has likely gone wrong, so an
        exception is thrown
        
        layer_name: The layer to get workers from
        
        Return:     A worker that is able to do work in that layer, None if all are busy
        Exception:  No workers are on the layer
    """
    def call(self, layer_name):
        workers = self.model.get_workers_by_layer(layer_name)
        if len(workers) == 0:
            raise NoWorkers(layer_name)

        # TODO filter busy workers
        # TODO intelligent prioritization (nodes good at networking get tasks that need networking)
        # TODO return None if all are busy
        return random.choice(workers)

