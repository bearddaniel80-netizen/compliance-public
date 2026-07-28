from .base.table_writer import TableWriter
import sqlite3

from ....models import OutputFormat
from ..report_models import ReporterRole
from ..report_registry import reporter
@reporter(
    formats=[
        OutputFormat.SQLITE,
    ],
    role=ReporterRole.WRITER,
)
class SqliteWriter(
    TableWriter
):

    def connect(
        self,
    ):

        return sqlite3.connect(
            self.destination
        )