from .pipeline.report_models import (
    ReportContext,
    ReportData,
)
from .pipeline.factory import ReportPipelineFactory
from ..pipeline.context import PipelineContext
from ..models import OutputFormat

def report(
    context: PipelineContext, output_format: OutputFormat
):

    report_context = (
        ReportContext(
            execution_context=context,
            report_data=ReportData(),
            output_format=output_format
        )
    )

    pipeline = ReportPipelineFactory.create(report_context)

    pipeline.run(
        report_context
    )
