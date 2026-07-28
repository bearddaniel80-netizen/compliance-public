import csv
from io import StringIO
from aql_link.core.base import StdinSource
from aql_link.core.builder import build_model, infer_schema
from aql_link.core.dataset import Dataset

class CsvSource(StdinSource):
    def __init__(self, raw: str):
        self.raw = raw
        self._rows = list(csv.DictReader(StringIO(raw)))

    def as_rows(self):
        return self._rows

    @classmethod
    def from_file(cls, filename: str):
        with open(filename, "r", newline="") as f:
            reader = f.read()

        return cls(reader)

    @classmethod
    def from_raw(cls, raw):
        return cls(raw)

    def to_dataset(self):
        rows = self.parse()  # list[dict] or dataclass
        return Dataset(rows, self.infer_model(rows))
 
    def _convert(self, v):
        if v is None or v == "":
            return None

        v = v.strip()

        if v.isdigit():
            return int(v)

        try:
            return float(v)
        except ValueError:
            pass

        if v.lower() in ("true", "false"):
            return v.lower() == "true"

        return v   
    
    def _infer_types(self, row):
        return {k: self._convert(v) for k, v in row.items()}
    
    def parse(self):
        import csv, io
        reader = csv.DictReader(io.StringIO(self.raw))

        if not reader.fieldnames or len(reader.fieldnames) < 1:
            raise ValueError("Invalid CSV")

        return [self._infer_types(row) for row in reader]



    def infer_model(self, schema):
        schema = infer_schema(schema)
        return build_model("CsvRow", schema)
        
    def schema(self):
        sample = self._rows[0] if self._rows else {}
        return infer_schema(sample)