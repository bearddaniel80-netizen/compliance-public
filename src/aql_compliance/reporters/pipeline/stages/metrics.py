from .base import PipelineStage
from ..report_models import (
    ReportContext,
    StatusType,
    FailureModel,
    PerformanceModel,
    SummaryModel
)

class MetricsStage(
    PipelineStage
):

    def run(
        self,
        report_context: ReportContext,
    ):
        failures = []
        query_by_time = []

        summary = report_context.execution_context.metadata["summary"]
        summary_mdl = SummaryModel(
            passed = summary["passed"],
            failed = summary["failed"],
            skipped = summary["skipped"],
            total = summary["total"],
            duration_ms = summary["duration_ms"],
            pass_rate = summary["passed"] / summary["total"] * 100
        )

        results = report_context.execution_context.results
        
        for result in results:
            if not result.passed and not result.skipped:
                failure = FailureModel(
                    manifest=result.name,
                    query=result.query,
                    error=result.error
                )
                failures.append(failure)
            elif result.passed:
                perf = PerformanceModel(
                    manifest=result.name,
                    query=result.query,
                    duration_ms=result.duration_ms,
                )
                query_by_time.append(perf)
        
        data = report_context.report_data
        data.summary=summary_mdl
        data.failures=failures
        data.performance=query_by_time

    def _status(self, result):
        if result.passed:
            return StatusType.PASS
        elif result.skipped:
            return StatusType.SKIP
        return StatusType.FAIL
        