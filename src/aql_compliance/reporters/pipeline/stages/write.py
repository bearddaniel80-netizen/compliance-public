from .base import PipelineStage
from ..report_models import ReportContext
from pathlib import Path

class WriteStage(
    PipelineStage
):

    def __init__(
        self,
        writer,
    ):
        self.writer = writer()
        
    def run(
        self,
        report_context: ReportContext,
    ):
            
        self.writer.write(
            report_context.artifact
        )