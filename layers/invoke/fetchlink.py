from multiprocessing.dummy import Pool
from tools.com.client import SocketClient


class FetchLink:
    def __init__(self, config, handler, name):
        self.config = config
        self.pool = Pool(config.get_int("FetchThreadCount"))
        self.fetch_host = config.get_str("FetchHost")
        self.fetch_port = config.get_int("FetchPort")
        self.name = name
        self.handler = handler

    def _fetch(self, query):
        with SocketClient(self.fetch_host, self.fetch_port, self.name) as client:
            res = client.send_message("FETCH", query.to_dict())

            if res.status == "WAIT":
                return  # cast out any messages that need to be waited for

            if res.status != "OKAY":
                print(str(res))
                return

        return res.content

    def _send_query(self, query):
        data = self._fetch(query)
        self.handler.send(data)

    def queue_queries_from_iter(self, iterator):
        self.pool.imap(self._send_query, iterator)
