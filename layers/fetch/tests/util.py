from limiters.limited_limiter import UnlimitedLimiter
from managers.http_manager import HttpManager
from source import Source


def get_fake_source():
    return Source("source1", UnlimitedLimiter(), HttpManager())