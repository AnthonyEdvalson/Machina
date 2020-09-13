import ssl

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster, Session

from tools.config.config import Config


class ScyllaConnection:
    def __init__(self, config: Config):
        self.config = config.select("scylla")

        ssl_options = {
            'ca_certs': config["ca_path"],
            'ssl_version': ssl.PROTOCOL_TLSv1_2
        }

        auth_provider = PlainTextAuthProvider(
            username=self.config["username"],
            password=self.config["password"])

        cluster = Cluster(
            contact_points=self.config["contacts"],
            port=self.config.get("port", 9042),
            auth_provider=auth_provider,
            ssl_options=ssl_options)

        self.cluster = cluster

    def connect(self, keyspace) -> Session:
        return self.cluster.connect(keyspace)

    def close(self):
        self.cluster.shutdown()
