
"""
    Alpha is the default application protocol used for inter-node socket connections
    It's loosely based on HTTP. Each message has 3 sections, binary data, header data, and content
    binary data is extra information that is only useful to the protocol (message lengths)
    header data contains string information about the message, who sent it, how it's formatted, etc.
    content is the payload of the data

    Request:
    ===================================
    <frame length (long)>
    <layer>/<task>
    Format: <message format code>
    Sender: <name of client>
    Action: <action to take>

    <data>
    ===================================

    Response:
    ===================================
    <frame length (long)>
    <layer>/<task>
    Format: <message format code>
    Sender: <name of server>
    Status: <status>

    <data>
    ===================================

    common statuses:

    OKAY
        Everything went as planned, data in response
    WAIT
        Can't process now, try later
    FAIL
        Can't process due to an anticipated issue
    ERROR
        Can't process due to unanticipated issue
"""
import struct
from typing import Union

from tools.com import formatting

SECTION_DELIM = ":"
MAJOR_DELIM = "-"
ACTION_DELIM = "/"
PREFIX = "A"
ALL_DELIMS = {SECTION_DELIM, MAJOR_DELIM, ACTION_DELIM}


class Path:

    @staticmethod
    def from_str(string: str) -> 'Path':
        sections = string.split(SECTION_DELIM)
        assert sections[0] == PREFIX
        major = sections[1].split(MAJOR_DELIM)
        action_path = sections[2].split(ACTION_DELIM)

        return Path(major[0], major[1], action_path)

    @staticmethod
    def empty() -> 'Path':
        return Path("", "", [])

    def __init__(self, machine: str, layer: str, action_path: Union[str, list]):

        assert not any((c in ALL_DELIMS) for c in machine)
        assert not any((c in ALL_DELIMS) for c in layer)
        if type(action_path) is list:
            for s in action_path:
                assert not any((c in ALL_DELIMS) for c in s)
        else:
            assert not any((c in ALL_DELIMS) for c in action_path)

        self.machine = machine
        self.layer = layer
        self.action_path = action_path if type(action_path) is list else [action_path]

    def to_arr(self):
        return [self.machine, self.layer] + self.action_path

    def __str__(self):
        return "".join([PREFIX, SECTION_DELIM,
                        self.machine, MAJOR_DELIM,
                        self.layer, SECTION_DELIM,
                        ACTION_DELIM.join(self.action_path)])

    def __repr__(self):
        return self.__str__()


class Flow:
    @classmethod
    def from_socket(cls, socket):
        len_bytes = socket.recv(4)

        if len_bytes == b'':
            return None

        frame_len = struct.unpack('>L', len_bytes)[0]

        frame = socket.recv(frame_len)
        blocks = frame.split(b"\n\n", 1)
        headers = blocks[0].decode().split("\n")

        path = Path.from_str(headers[1])
        format = headers[2]

        parsed_headers = {}
        for header in headers[3:]:
            key, val = header.split(":")
            parsed_headers[key.strip()] = val.strip()

        raw = blocks[1]

        f = Flow(content=formatting.deserialize(raw, format), path=path, format=format, auto_set_raw=False, **parsed_headers)
        f.raw = raw
        f.foreign_ip = socket.getpeername()[0]
        f.foreign_port = socket.getpeername()[1]
        return f

    def __init__(self, path: Path, format: str, content: any=None, auto_set_raw=True, **headers):

        self.format = format
        self.headers = headers
        self.path = path
        self.content = content

        self.closed = False

        self.foreign_ip = None
        self.foreign_port = None

        if auto_set_raw:
            self.raw = formatting.serialize(content, format)

    def to_bytes(self):
        msg = "{}\n".format(self.path)
        msg += "{}\n".format(self.format)
        for key, value in self.headers.items():
            msg += "{}: {}\n".format(key, value)

        msg += "\n"
        msg = b'\n' + msg.encode() + self.raw

        msg = struct.pack('>I', len(msg)) + msg

        return msg

    def __str__(self):
        msg = self.raw
        return msg if len(msg) < 200 else msg[:200] + b'...'
