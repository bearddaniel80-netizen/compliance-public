import csv

from io import StringIO

from ..report_models import (
    FileArtifact, 
    ReporterRole,
    ReportContext
)

from ....models import OutputFormat 
from ..report_registry import reporter

@reporter(
    formats=[
        OutputFormat.CSV,
    ],
    role=ReporterRole.RENDERER,
)
class CsvRenderer:

    def render(
        self,
        report_context: ReportContext,
    ) -> FileArtifact:

        buffer = StringIO()

        writer = csv.writer(
            buffer
        )

        writer.writerow(
            [
                "name",
                "query",
                "passed",
                "skipped",
                "duration_ms",
                "error",
            ]
        )

        for result in report_context.execution_context.results:

            writer.writerow(
                [
                    result.name,
                    result.query.text.replace(",", ""),
                    result.passed,
                    result.skipped,
                    result.duration_ms,
                    result.error,
                ]
            )

        report_context.artifact =  FileArtifact(
            content=buffer.getvalue(),
            output_file="report.csv"
        )