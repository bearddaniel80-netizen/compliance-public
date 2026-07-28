from .base import PipelineStage
from ..report_models import ReportContext
from pathlib import Path
import webbrowser

class OpenBrowserStage(
    PipelineStage
):

    def run(
        self,
        report_context: ReportContext,
    ):
        path = Path.cwd() / report_context.output_file
        webbrowser.open(
            Path(path)
            .resolve()
            .as_uri()
        )