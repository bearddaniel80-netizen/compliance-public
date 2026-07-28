import time
from .base import PipelineStage
from ..context import PipelineContext

class ProfileStage(
    PipelineStage
):

    def __init__(
        self,
        wrapped_stage: PipelineStage,
    ):
        self.wrapped_stage = wrapped_stage

    @property
    def name(self) -> str:
        return (
            f"Profile({self.wrapped_stage.name})"
        )

    def run(
        self,
        context: PipelineContext,
    ) -> None:

        start = time.perf_counter()

        self.wrapped_stage.run(
            context
        )

        duration_ms = int(
            (
                time.perf_counter()
                - start
            ) * 1000
        )

        timings = context.metadata.setdefault(
            "stage_timings",
            {}
        )

        timings[
            self.wrapped_stage.name
        ] = duration_ms