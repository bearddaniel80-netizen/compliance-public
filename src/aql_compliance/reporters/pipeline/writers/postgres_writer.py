from .base.table_writer import TableWriter

from ....models import OutputFormat
from ..report_models import ReporterRole
from ..report_registry import reporter
@reporter(
    formats=[
        OutputFormat.POSTGRES,
    ],
    role=ReporterRole.WRITER,
)
class PostgresWriter( TableWriter ):
    def connect(
        self,
    ):

        raise NotImplementedError(
            "Postgres support "
            "coming soon"
        )