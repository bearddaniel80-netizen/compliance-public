import avro.datafile
import avro.io
import avro.schema


from aql_link.core.base import StdinSource
from aql_link.core.builder import build_model, infer_schema
from aql_link.core.dataset import Dataset

# Apache Avro is a binary data serialization format designed for:
# compact storage
# fast transport
# schema evolution
# distributed systems
# It is heavily used with:
# Apache Kafka
# Apache Hadoop
# data lakes
# streaming pipelines
# ETL systems
# Think of it as:
# JSON semantics
# but binary + typed + schema-aware

class AvroSource:

    def __init__(self, rows):
        self._rows = rows

    @classmethod
    def from_file(cls, filename: str):

        rows = []

        with open(filename, "rb") as f:
            reader = avro.datafile.DataFileReader(
                f,
                avro.io.DatumReader()
            )

            for record in reader:
                rows.append(record)

            reader.close()

        return cls(rows)

    def as_rows(self):
        return self._rows

    def to_dataset(self):
        return Dataset(
            self._rows,
            self.infer_model(self._rows[0])
        )

    def infer_model(self, sample):
        schema = infer_schema(sample)
        return build_model("AvroRow", schema)

    def schema(self):
        return infer_schema(self._rows[0])