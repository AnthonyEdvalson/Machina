from limiter import Limiter


class UnlimitedLimiter(Limiter):
    def over_used(self):
        return False
