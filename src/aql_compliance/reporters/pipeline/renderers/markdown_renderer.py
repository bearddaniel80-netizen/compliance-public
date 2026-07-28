from ..report_models import (
    FileArtifact, ReporterRole, ReportContext
)

from ....models import OutputFormat
from ..report_registry import reporter

@reporter(
    formats=[
        OutputFormat.MARKDOWN,
    ],
    role=ReporterRole.RENDERER,
)
class MarkdownRenderer:

    def render(
        self,
        report_context: ReportContext,
    ) -> FileArtifact:

        lines = []

        lines.append(
            "# AQL Compliance Results"
        )

        lines.append("")

        summary = report_context.report_data.summary

        lines.append(
            f"📊 Total: {summary.total}"
        )

        lines.append(
            f"✅ Passed: {summary.passed}"
        )

        lines.append(
            f"❌ Failed: {summary.failed}"
        )

        lines.append(
            f"⏭️ Skipped: {summary.skipped}"
        )

        lines.append(
            f"⏱️ Duration: {summary.duration_ms} ms"
        )

        lines.append(
            f"📊 Pass rate: {summary.pass_rate}"
        )

        lines.append("")
        lines.append("## Results")
        lines.append("")

        lines.append(
            "| Status | Name | Duration (ms) | Query |"
        )

        lines.append(
            "|---------|------|---------------|-------|"
        )

        for result in report_context.execution_context.results:

            if result.skipped:

                status = "⏭️"

            elif result.passed:

                status = "✅"

            else:

                status = "❌"

            lines.append(
                "| "
                f"{status} | "
                f"{result.name} | "
                f"{result.duration_ms} | "
                f"`{result.query.text}` |"
            )

        failures = report_context.report_data.failures

        if failures:

            lines.append("")
            lines.append(
                "## Failures"
            )
            lines.append("")

            for failure in failures:

                lines.append(
                    f"### {failure.manifest}"
                )

                lines.append("")

                lines.append(
                    f"**Query:** "
                    f"`{failure.query.text}`"
                )

                lines.append("")

                lines.append(
                    f"**Error:** "
                    f"{failure.error}"
                )

                lines.append("")

        if report_context.execution_context.profile:
            results = sorted(
                report_context.report_data.performance,
                key=lambda r: r.duration_ms,
                reverse=True,
            )
            lines.append("## Query Performance")
            for result in results:
                lines.append("")
                lines.append(f"Name: {result.manifest}`")
                lines.append("")
                lines.append(f"**Query:** `{result.query}`")
                lines.append("")
                lines.append(f"Duration: {result.duration_ms}`")


        report_context.artifact =  FileArtifact(
            content="\n".join(
                lines
            ),
            output_file="report.md"
        )