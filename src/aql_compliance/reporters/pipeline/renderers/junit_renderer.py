import xml.etree.ElementTree as ET

from ..report_models import (
    FileArtifact,
    ReporterRole,
    ReportContext
)

from ....models import (
    OutputFormat,
)

from ..report_registry import (
    reporter,
)


@reporter(
    formats=[
        OutputFormat.JUNIT,
    ],
    role=ReporterRole.RENDERER,
)
class JUnitRenderer:

    def render(
        self,
        report_context: ReportContext,
    ) -> FileArtifact:

        root = ET.Element(
            "testsuites"
        )
        summary = report_context.report_data.summary

        testsuite = ET.SubElement(
            root,
            "testsuite",
            name="aql-compliance",
            tests=str(
                summary.total
            ),
            passed=str(
                summary.passed
            ),
            failures=str(
                summary.failed
            ),
            skipped=str(
                summary.skipped
            ),
            time=str(
                summary.duration_ms
            ),
            pass_rate=str(
                summary.pass_rate
            ),
        )

        self._profile(
            testsuite,
            report_context,
        )

        for result in report_context.execution_context.results:

            testcase = ET.SubElement(
                testsuite,
                "testcase",
                name=result.name,
                classname="aql",
                time=str(
                    result.duration_ms
                ),
            )

            ET.SubElement(
                testcase,
                "system-out",
            ).text = result.query.text

            if result.skipped:

                ET.SubElement(
                    testcase,
                    "skipped",
                )

            elif not result.passed:

                failure = ET.SubElement(
                    testcase,
                    "failure",
                    message=(
                        result.error
                        or "Failed"
                    ),
                )

                failure.text = (
                    result.query.text
                )

        xml = ET.tostring(
            root,
            encoding="unicode",
        )

        report_context.artifact =  FileArtifact(
            content=xml,
            output_file="report.xml"
        )

    def _profile(
        self,
        testsuite,
        report_context,
    ):

        if report_context.execution_context.profile == False:
            return

        profile = ET.SubElement(
            testsuite,
            "profile",
        )

        results = sorted(
            report_context.report_data.performance,
            key=lambda r: r.duration_ms,
            reverse=True,
        )

        for result in results:

            node = ET.SubElement(
                profile,
                "query-performance",
                name=str(result.manifest),
                time=str(result.duration_ms),
            )

            node.text = result.query.text
