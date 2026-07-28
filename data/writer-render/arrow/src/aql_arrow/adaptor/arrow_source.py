import pyarrow as pa
import pyarrow.ipc as ipc

from aql_link.core.base import StdinSource
from aql_link.core.builder import build_model, infer_schema
from aql_link.core.dataset import Dataset

class ArrowSource:

    def __init__(self, table):
        self._table = table

    @classmethod
    def from_file(cls, filename: str):

        with pa.memory_map(filename, "r") as source:

            reader = ipc.RecordBatchFileReader(source)

            table = reader.read_all()

        return cls(table)

    def as_rows(self):
        return self._table.to_pylist()

    def to_dataset(self):

        rows = self.as_rows()

        return Dataset(
            rows,
            self.infer_model(rows[0])
        )

    def infer_model(self, sample):
        schema = infer_schema(sample)
        return build_model("ArrowRow", schema)

    def schema(self):
        return self._table.schema