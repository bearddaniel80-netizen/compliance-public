from .base import PipelineStage
from ..context import PipelineContext

class MetricsStage(PipelineStage):

    @property
    def name(self):
        return "MetricsStage"

    def run(
        self,
        context: PipelineContext,
    ) -> None:
      
        passed = sum(
            1
            for r in context.results
            if r.passed
        )

        failed = sum(
            1
            for r in context.results
            if not r.passed
            and not r.skipped
        )

        skipped = sum(
            1
            for r in context.results
            if r.skipped
        )

        duration_ms = sum(
            r.duration_ms
            for r in context.results
        )

        context.metadata[
            "summary"
        ] = {
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "total": len(
                context.results
            ),
            "duration_ms": duration_ms,
        }