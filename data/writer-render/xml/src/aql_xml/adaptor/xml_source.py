import xml.etree.ElementTree as ET
from aql_link.core.base import StdinSource
from aql_link.core.builder import build_model, infer_schema
from aql_link.core.dataset import Dataset

class XmlSource(StdinSource):
    def __init__(self, raw: str):
        self.raw = raw
        self.root = ET.fromstring(raw)

    def as_rows(self):
        rows = []

        for child in self.root:
            row = {}
            for elem in child:
                row[elem.tag] = elem.text
            rows.append(row)

        return rows

    @classmethod
    def from_file(cls, filename: str):
        with open(filename, "r") as f:
            data = f.read()

        return cls(data)

    @classmethod
    def from_raw(cls, raw):
        return cls(raw)

    def to_dataset(self):
        rows = self.parse()  # list[dict] or dataclass
        return Dataset(rows, self.infer_model(rows))
    
    def parse(self):
        from xml.etree import ElementTree as ET

        root = ET.fromstring(self.raw)
        return [self._flatten(root)]

    def _flatten(self, elem):
        return {
            "tag": elem.tag,
            "text": elem.text.strip() if elem.text else None,
            **elem.attrib
        }

    def infer_model(self, schema):
        schema = infer_schema(schema)
        return build_model("XmlRow", schema)

    def schema(self):
        rows = self.as_rows()
        sample = rows[0] if rows else {}
        return infer_schema(sample)