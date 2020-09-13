from tools.com.alpha import Path, Flow


class Task:
    @classmethod
    def from_request(cls, req: Flow):
        cls.path = req.path
        cls.data = req.content

        return cls

    def __init__(self, path: Path, data: any=None):
        self.path = path
        self.data = data
