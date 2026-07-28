from ..report_models import (
    TableArtifact, ReporterRole, ReportContext
)

from ....models import OutputFormat
from ..report_registry import reporter

@reporter(
    formats=[
        OutputFormat.ARROW,
        OutputFormat.AVRO,
        OutputFormat.DUCKDB,
        OutputFormat.MYSQL,
        OutputFormat.PARQUET,
        OutputFormat.POSTGRES,
        OutputFormat.SQLITE,
    ],
    role=ReporterRole.RENDERER,
)
class TableRenderer:
    def render(
        self,
        report_context: ReportContext,
    ) -> TableArtifact:

        tables = (        
        {
            "summary": [
                report_context.report_data.summary.to_dict()
            ],

            "failures": [
                x.to_dict()
                for x in report_context.report_data.failures
            ],

            "performance": [
                x.to_dict()
                for x in report_context.report_data.performance
            ],

            "queries": [
                x.to_dict()
                for x in report_context.report_data.queries
            ]
        }
        )
        report_context.artifact =  TableArtifact(
            tables=tables,
            output_file="report."+report_context.output_format
        )