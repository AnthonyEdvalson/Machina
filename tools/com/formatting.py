import datetime
import json
from enum import Enum

from tools.config.config import Config


def serialize(data, format):
    assert format in formats
    return formats[format].serialize(data)


def deserialize(data, format):
    assert type(data) is bytes
    return formats[format].deserialize(data)


class LooseJsonEncoder(json.JSONEncoder):
    def default(self, o):
        t = type(o)

        if isinstance(o, Enum):
            return o.value
        if t == datetime.timedelta:
            return o.total_seconds()
        if t == datetime.datetime:
            return o.timestamp()
        if t == Config:
            return o.as_dict()

        return dict(filter(lambda a: a[0][0] != "_", o.__dict__.items()))


class Json:
    def __init__(self):
        self.encoder = LooseJsonEncoder()

    def serialize(self, data):
        return self.encoder.encode(data).encode()

    def deserialize(self, data):
        return json.loads(data.decode())


class Text:
    def serialize(self, data):
        return str(data).encode()

    def deserialize(self, data):
        return data.decode()


class Bytes:
    def serialize(self, data):
        assert type(data) is bytes
        if data is None:
            return b''

        return data

    def deserialize(self, data):
        return data


formats = {
    "json": Json(),
    "text": Text(),
    "bytes": Bytes()
}
