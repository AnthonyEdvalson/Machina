import configparser
import os
import json

from tools.config.config import Config


class ConfigLoader:
    def __init__(self, path: str, mode: str):
        self.path = path
        self.mode = mode

    def load_ini(self) -> Config:
        print("Loading config.ini with mode {} from {}".format(self.mode, os.getcwd() + self.path))

        config_parser = configparser.ConfigParser()
        config_parser.read(self.path)

        data = {}
        self._try_load_section("Default", config_parser, data)
        self._try_load_section(self.mode, config_parser, data)

        assert len(data) > 0

        return self._make_config(data)

    def load_json(self) -> Config:
        data = json.load(open(self.path))
        mode_data = data["default"]
        mode_data.update(data[self.mode])

        return self._make_config(mode_data)

    def load_linked_json(self) -> Config:
        pass

    def _make_config(self, data: dict) -> Config:
        config = Config(data)
        print(config)
        return config

    def _try_load_section(self, section: str, config_parser: configparser, data: dict) -> bool:
        if section in config_parser:
            data.update(dict(config_parser.items(section)))
            return True
        return False
