from rich.table import Table
from rich.panel import Panel
from rich.console import Group

from ..report_models import (
    ConsoleArtifact, ReporterRole, ReportContext
)

from ....models import OutputFormat
from ..report_registry import reporter
@reporter(
    formats=[
        OutputFormat.RICH,
    ],
    role=ReporterRole.RENDERER,
)
class RichRenderer:

    def render(
        self,
        report_context: ReportContext,
    ) -> ConsoleArtifact:

        table = Table(
            title="AQL Compliance Results"
        )

        table.add_column(
            "Status"
        )

        table.add_column(
            "Name"
        )

        table.add_column(
            "Duration (ms)"
        )

        table.add_column(
            "Query"
        )

        table.add_column(
            "Error"
        )

        for result in report_context.execution_context.results:

            if result.skipped:

                status = "[yellow]SKIP[/]"

            elif result.passed:

                status = "[green]PASS[/]"

            else:

                status = "[red]FAIL[/]"

            table.add_row(status, result.name, str(result.duration_ms), result.query.text, result.error)

        summary = Panel.fit(
            (
                f"Total: {report_context.report_data.summary.total}\n"
                f"Passed: {report_context.report_data.summary.passed}\n"
                f"Failed: {report_context.report_data.summary.failed}\n"
                f"Skipped: {report_context.report_data.summary.skipped}\n"
                f"Duration: {report_context.report_data.summary.duration_ms} ms\n"
                f"Pass Rate: {report_context.report_data.summary.pass_rate}%\n"
            ),
            title="Summary",
        )

        if report_context.execution_context.profile:
            perfs = sorted(
                report_context.report_data.performance,
                key=lambda r: r.duration_ms,
                reverse=True,
            )
            perf = perfs[0]
            profile = Panel.fit(
                (
                    f"Name: {perf.manifest}\n"
                    f"Query: {perf.query.text}\n"
                    f"Duration: {perf.duration_ms}\n"
                ),
                title="Slowest Query",
            )

            report_context.artifact = ConsoleArtifact(
                renderable=Group(
                    summary,
                    profile,
                    table,
                )
            )
        else:
            report_context.artifact = ConsoleArtifact(
                renderable=Group(
                    summary,
                    table,
                )
            )