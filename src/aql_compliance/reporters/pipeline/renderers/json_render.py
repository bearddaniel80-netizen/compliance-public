import json

from ..report_models import (
    FileArtifact, 
    ReporterRole,
    ReportContext
)
from ....models import OutputFormat
from ..report_registry import reporter

@reporter(
    formats=[
        OutputFormat.JSON,
    ],
    role=ReporterRole.RENDERER,
)
class JsonRenderer:

    def render(
        self,
        report_context: ReportContext,
    ) -> FileArtifact:

        summary = report_context.report_data.summary
        failures = report_context.report_data.failures

        payload = {
            "summary": summary.to_dict(),
            "results": [ result.to_dict() for result in report_context.execution_context.results],
            "failures": [ failure.to_dict() for failure in failures ]
        }

        if report_context.execution_context.profile:
            results = sorted(
                report_context.report_data.performance,
                key=lambda r: r.duration_ms,
                reverse=True,
            )
            
            payload["query_performance"] = [ result.to_dict() for result in results ]


        report_context.artifact =  FileArtifact(
            content=json.dumps(
                payload,
                indent=2,
                default=str,
            ),
            output_file="report.json"
        )