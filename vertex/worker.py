from vertex.lease import Lease
from vertex.resources import Resources


class Worker:
    def __init__(self, name: str, server_port: int, resources: Resources, leases: [Lease]=None):
        self.name = name
        self.server_port = server_port
        self.resources = resources
        self.leases: [Lease] = leases if leases is not None else []

    """
        Returns the lease for a given layer on this worker, returns None if the layer has not be leased to this worker
    """
    def get_layer(self, layer: str) -> Lease:
        for lease in self.leases:
            if lease.layer == layer:
                return lease

    """
    def to_dict(self):
        return {
            "name": self.name,
            "server_port": self.server_port,
            "resources": self.resources.to_dict(),
            "leases": list(map(lambda l: l.to_dict(), self.leases))
        }
"""