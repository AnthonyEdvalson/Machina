import importlib

from source import Source
from tools.config.config import Config
from vertex.layer import Layer, route
from vertex.router import Router
from vertex.task import Task


class Fetch(Layer):
    def __init__(self, config: Config):
        self.full_config = config
        self.config = config.select("layers/fetch")
        self.sources = self.make_sources()

    def make_sources(self) -> [Source]:
        modules = self.config.get("modules")

        source_types = []

        for module in modules:
            source_types += importlib.import_module("modules.{}.sources".format(module)).sources

        sources = map(lambda s: s(self.config), source_types)
        return dict(map(lambda s: (s.name, s), sources))

    # ROUTES

    @route
    def over_quota(self, task: Task):
        return self.sources[task.path[-2]].over_used()

    @route
    def fetch(self, task: Task):
        return self.sources[task.path[-2]].fetch(task.path[-1], task.data)

    def get_router(self):
        return Router("Fetch", {
                "OverQuota": self.over_quota,
                "Fetch": self.fetch
            })
