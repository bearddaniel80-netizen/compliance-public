from rich.console import Console

from ....models import OutputFormat
from ..report_models import ReporterRole
from ..report_registry import reporter

@reporter(
    formats=[
        OutputFormat.RICH,
    ],
    role=ReporterRole.WRITER,
)
class ConsoleWriter:

    def write(
        self,
        artifact,
    ):
        Console().print(
            artifact.renderable
        )