from limiter import PercentLimiter
import time


"""
    RateLimiter is a common limiter that only allows for a certain number of requests to be made over a  period of time
    it requires an external data source to keep track of usage

    throttling is used to tweak the behavior:
    If enabled (default) it will limit to a regular flow of queries throughout the day
    If disabled, it will allow all requests for the entire day through at any time, this should be used if
    large bursts of data are needed, instead of a slow stream

    padding is the percent of the quota that will not be used, to reduce the risk of going over budget
"""


class RateLimiter(PercentLimiter):
    def __init__(self, data_source, quota, days, throttled=True, padding=0.05):
        self.data_source = data_source
        self.quota = (quota / days) * (1 - padding)
        self.timescale = days
        self.throttled = throttled

    def query_success(self, weight=1):
        self.data_source.add(weight)

    def adjusted_quota(self):
        if self.throttled:

            # day ratio is set so that 0 = 0:00:00 UTC, 1 = 23:59:59 UTC
            # this way, x% of the quota is available x% of the way through the day, so an even distribution
            day_ratio = (time.time() % 86400) / 3600
            return self.quota * day_ratio
        else:
            # no throttling, allow the full quota to be available at all times
            return self.quota

    def percent_used(self):
        return self.data_source.get() / self.adjusted_quota()
