from .base.table_writer import TableWriter
from ....module_loader import load

from ....models import OutputFormat
from ..report_models import ReporterRole
from ..report_registry import reporter
@reporter(
    formats=[
        OutputFormat.DUCKDB,
    ],
    role=ReporterRole.WRITER,
)
class DuckDbWriter(
    TableWriter
):

    def connect(
        self,
    ):
        load("duckdb")
        import duckdb

        return duckdb.connect(
            self.destination
        )