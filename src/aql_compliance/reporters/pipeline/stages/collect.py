from .base import PipelineStage
from ..report_models import (
    ReportContext,
    StatusType,
    QueryModel,
)

class CollectStage(
    PipelineStage
):

    def run(
        self,
        report_context: ReportContext,
    ):
        queries = []
        results = report_context.execution_context.results
        
        for result in results:
            query = QueryModel(
                name=result.name,
                query=result.query,
                status=self._status(result),
                duration_ms=result.duration_ms,
                error=result.error
            )
            queries.append(query)
        
        data = report_context.report_data
        data.queries=queries

    def _status(self, result):
        if result.passed:
            return StatusType.PASS
        elif result.skipped:
            return StatusType.SKIP
        return StatusType.FAIL
        