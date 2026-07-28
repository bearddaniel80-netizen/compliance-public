from pathlib import Path

from ....models import OutputFormat
from ..report_models import ReporterRole
from ..report_registry import reporter

@reporter(
    formats=[
        OutputFormat.CSV,
        OutputFormat.GITHUB,
        OutputFormat.HTML,
        OutputFormat.JSON,
        OutputFormat.JUNIT,
        OutputFormat.MARKDOWN,
        OutputFormat.PDF,
    ],
    role=ReporterRole.WRITER,
)
class FileWriter:

    def write(
        self,
        artifact,
    ):
        self.destination = (
            Path.cwd() / artifact.output_file
        )

        if artifact.binary:

            self.destination.write_bytes(
                artifact.content
            )

        else:

            self.destination.write_text(
                artifact.content,
                encoding="utf-8",
            )