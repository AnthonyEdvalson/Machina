class Resources:
    def __init__(self, ram_gb: float, cpu_cores: int, gpu_cores: int, storage_gb: float, network_mbs: float):
        self.ram_gb = ram_gb
        self.cpu_cores = cpu_cores
        self.gpu_cores = gpu_cores
        self.storage_gb = storage_gb
        self.network_mbs = network_mbs

    def can_contain(self, resources) -> bool:
        rd = resources.as_dict()
        for k, v in self.as_dict().items():
            if v < rd[k]:
                return False
        return True

    def __add__(self, other):
        assert other is Resources
        od = other.as_dict()

        sum_dict = {}

        for k, v in self.as_dict().items():
            sum_dict[k] = v + od[k]

        return Resources(**sum_dict)

    def __sub__(self, other):
        assert other is Resources
        od = other.as_dict()

        sum_dict = {}

        for k, v in self.as_dict().items():
            sum_dict[k] = v - od[k]

        return Resources(**sum_dict)

    def __eq__(self, other):
        od = other.as_dict()

        for k, v in self.as_dict().items():
            if v != od[k]:
                return False
        return True

    def __str__(self):
        return str(self.as_dict())

    def as_dict(self) -> dict:
        return {
            "ram_gb": self.ram_gb,
            "cpu_cores": self.cpu_cores,
            "gpu_cores": self.gpu_cores,
            "storage_gb": self.storage_gb,
            "network_mbs": self.network_mbs
        }
