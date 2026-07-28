from .base import PipelineStage
from ..context import PipelineContext
from ...models import OutputFormat
from ...reporters.reporter import report

class ReportStage(
    PipelineStage
):

    @property
    def name(self):
        return "ReportStage"

    def __init__(
        self,
        output_format: OutputFormat,
        profile=False,
    ):
        self.output_format = output_format
        self.profile = profile

    def run(
        self,
        context: PipelineContext,
    ):
        report(context, self.output_format)