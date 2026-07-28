from .base.table_writer import TableWriter

from ....models import OutputFormat
from ..report_models import ReporterRole
from ..report_registry import reporter
@reporter(
    formats=[
        OutputFormat.MYSQL,
    ],
    role=ReporterRole.WRITER,
)
class MySqlWriter( TableWriter ):
    def connect(
        self,
    ):

        raise NotImplementedError(
            "Mysql support "
            "coming soon"
        )