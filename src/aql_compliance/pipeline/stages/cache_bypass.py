from .base import PipelineStage
from ..context import PipelineContext

from ...models import (
    TestResult,
)


class CacheBypassStage(
    PipelineStage
):

    @property
    def name(self):
        return "CacheBypassStage"

    def run(
        self,
        context: PipelineContext,
    ) -> None:

        if not context.metadata.get(
            "cache_hit"
        ):
            return

        context.results = [
            TestResult(**item)
            for item in context.metadata[
                "cached_results"
            ]
        ]

        context.metadata[
            "pipeline_stop"
        ] = True