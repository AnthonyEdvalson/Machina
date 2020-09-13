import uuid
from datetime import timedelta, datetime
from enum import Enum

from vertex.resources import Resources


class LeaseState(Enum):
    NOTSIGNED = 0  # Lease has been created, but has not been signed yet
    SIGNED = 1  # Lease has been signed, and will expire in the designated amount of time. Worker is not yet ready to accept requests
    ACTIVE = 2  # Lease has been signed, and the worker it is meant for is prepared to accept requests


class Lease:
    def __init__(self, layer: str, resources: Resources, lessee: str=None,
                 duration: (timedelta, int)=None, start: (datetime, int)=None, state=LeaseState.NOTSIGNED, uid=None):

        if duration is None:
            self.duration = timedelta(hours=2)
        elif type(duration) is int or type(duration) is float:
            self.duration = timedelta(seconds=duration)
        elif type(duration) is timedelta:
            self.duration = duration
        else:
            raise Exception("Invalid type for duration " + str(type(duration)))

        if type(start) is int or type(start) is float:
            self.start = datetime.utcfromtimestamp(start)
        elif type(start) is datetime or start is None:
            self.start = start
        else:
            raise Exception("Invalid type for start " + str(type(start)))

        self.lessee = lessee
        self.layer = layer
        self.resources = resources
        self.state = state if type(state) == LeaseState else LeaseState(state)
        self.uid = str(uuid.uuid4()) if uid is None else uid

    def sign(self, lessee: str) -> None:
        self.lessee = lessee
        self.start = datetime.now()
        self.state = LeaseState.SIGNED

    def activate(self):
        self.state = LeaseState.ACTIVE

    def is_valid(self):
        if self.state != LeaseState.ACTIVE:
            return False

        now = datetime.utcnow()
        return self.start < now < (self.start + self.duration)

    def remaining_time(self, time: datetime=None) -> timedelta:
        now = time if time is not None else datetime.utcnow()
        return (self.start - now) + self.duration
