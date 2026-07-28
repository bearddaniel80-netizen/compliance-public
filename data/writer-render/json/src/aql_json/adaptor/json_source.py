import json

from aql_link.core.base import StdinSource
from aql_link.core.builder import build_model, infer_schema
from aql_link.core.dataset import Dataset

class JsonFileSource(StdinSource):
    def __init__(self, raw: str):
        self._data = raw

    @classmethod
    def from_file(cls, filename):
        with open(filename, "r") as f:
            raw = json.load(f)
        return cls(raw)

    def to_dataset(self):
        return Dataset(self._data, self.infer_model(self._data))

    def infer_model(self, schema):
        schema = infer_schema(schema)
        return build_model("JsonRow", schema)

class JsonStdinSource(StdinSource):
    def __init__(self, raw: str):
        self.raw = raw
        self._data = json.loads(raw)

    def as_rows(self):
        if isinstance(self._data, list):
            return self._data
        return [self._data]


    @classmethod
    def from_raw(cls, raw):
        return cls(raw)

    def to_dataset(self):
        rows = self.parse()  # list[dict] or dataclass
        return Dataset(rows, self.infer_model(rows))

    def parse(self):
        data = json.loads(self.raw)

        if isinstance(data, list):
            return data
        return [data]

    def infer_model(self, schema):
        schema = infer_schema(schema)
        return build_model("JsonRow", schema)
        
    def schema(self):
        sample = self.as_rows()[0]
        return infer_schema(sample)        