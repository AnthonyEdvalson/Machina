from limiter import Limiter


class LimitedLimiter(Limiter):
    def over_used(self):
        return True
