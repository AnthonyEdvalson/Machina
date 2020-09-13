class Config:
    def __init__(self, data: any=None):
        assert type(data) == dict
        self._data = {} if data is None else data

    def get(self, key: str, default: any=None) -> any:
        d, key = self.resolve(key)
        return d[key] if key in d else default

    def __getitem__(self, key: str) -> any:
        d, key = self.resolve(key)
        return d[key]

    def alter(self, key: str, value: any, exists: bool=True) -> None:
        d, key = self.resolve(key)

        if key not in d and exists:
            raise self.not_found(key, d, "If you want to create a new key when it doesnt exist, set exists to False")

        d[key] = value
        print("!!! Config Altered ({}: {})".format(key, value))

    def resolve(self, key):
        keys = key.split("/")
        key = keys[-1]

        d = self._data
        for k in keys[:-1]:
            if k not in d:
                raise self.not_found(key, d, "Cannot traverse")
            d = d[k]
            if type(d) != dict:
                raise KeyError("'{}' is a {}, not a dictionary, cannot traverse to it".format(key, str(type(d))))

        return d, key

    def not_found(self, key, d, msg):
        return KeyError("'{}' not found in {}. {}".format(key, ", ".join(list(d.keys())), msg))

    def select(self, key: str) -> 'Config':
        return Config(self[key])

    def as_dict(self) -> dict:
        return self._data.copy()

    def __str__(self) -> str:
        return "Current Config: {}".format(str(self._data))

    def __eq__(self, other) -> bool:
        if type(other) is not Config:
            return False

        return self._data == other._data
