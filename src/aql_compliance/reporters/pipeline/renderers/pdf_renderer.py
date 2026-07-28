from ..report_models import (
    FileArtifact, ReporterRole, ReportContext
)
from io import BytesIO

from ....models import OutputFormat
from ..report_registry import reporter
from ....module_loader import load

@reporter(
    formats=[
        OutputFormat.PDF,
    ],
    role=ReporterRole.RENDERER,
)
class PdfRenderer:

    def render(
        self,
        report_context: ReportContext,
    ) -> FileArtifact:

        buffer = BytesIO()
        load("reportlab")
        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            PageBreak,
        )

        from reportlab.lib.styles import (
            getSampleStyleSheet,
        )

        document = SimpleDocTemplate(
            buffer
        )

        styles = (
            getSampleStyleSheet()
        )

        content = []

        content.append(
            Paragraph(
                report_context.execution_context.manifest_name,
                styles["Title"],
            )
        )

        content.append(
            Spacer(
                1,
                12,
            )
        )

        content.append(
            Paragraph(
                "Summary",
                styles["Heading2"],
            )
        )

        summary = report_context.report_data.summary

        content.append(
            Paragraph(
                (
                    f"Total: "
                    f"{summary.total}<br/>"
                    f"Passed: "
                    f"{summary.passed}<br/>"
                    f"Skipped: "
                    f"{summary.skipped}<br/>"
                    f"Failed: "
                    f"{summary.failed}<br/>"
                    f"Duration: "
                    f"{summary.duration_ms} ms<br/>"
                    f"Pass Rate: "
                    f"{summary.pass_rate} %"
                ),
                styles["BodyText"],
            )
        )

        content.append(
            Spacer(
                1,
                12,
            )
        )

        if report_context.execution_context.profile:

            results = sorted(
                report_context.report_data.performance,
                key=lambda r: r.duration_ms,
                reverse=True,
            )

            content.append(
                Paragraph(
                    "Query Performance",
                    styles["Heading2"],
                )
            )

            for result in results:
                content.append(
                    Paragraph(
                        (
                            f"{result.manifest}<br/>"
                            f"{result.query.text}<br/>"
                            f"{result.duration_ms} ms"
                        ),
                        styles["BodyText"],
                    )
                )

                content.append(
                    Spacer(
                        1,
                        12,
                    )
                )

        content.append(
            Paragraph(
                "Results",
                styles["Heading2"],
            )
        )

        for result in report_context.execution_context.results:

            status = (
                "PASS"
                if result.passed
                else "FAIL"
            )

            if result.skipped:
                status = "SKIP"

            content.append(
                Paragraph(
                    (
                        f"<b>[{status}]</b> "
                        f"{result.query.text} "
                        f"{result.duration_ms}ms"
                    ),
                    styles["BodyText"],
                )
            )

            if result.error:

                content.append(
                    Paragraph(
                        (
                            f"Error: "
                            f"{result.error}"
                        ),
                        styles["Code"],
                    )
                )

            content.append(
                Spacer(
                    1,
                    4,
                )
            )

        document.build(
            content
        )

        pdf_bytes = (
            buffer.getvalue()
        )

        report_context.artifact =  FileArtifact(
            content=pdf_bytes,
            binary=True,
            output_file="report.pdf"
        )