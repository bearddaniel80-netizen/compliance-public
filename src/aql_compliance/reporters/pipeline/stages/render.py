from .base import PipelineStage
from ..report_models import ReportContext

class RenderStage(
    PipelineStage
):

    def __init__(
        self,
        renderer,
    ):
        self.renderer = renderer()

    def run(
        self,
        context: ReportContext,
    ):
        context.content = self.renderer.render(report_context=context)
        