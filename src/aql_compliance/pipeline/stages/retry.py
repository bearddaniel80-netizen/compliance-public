from .base import PipelineStage
from ...exceptions import RetryableError
from ..context import PipelineContext

class RetryStage(
    PipelineStage
):

    def __init__(
        self,
        wrapped_stage: PipelineStage,
        retries: int = 3,
    ):
        self.wrapped_stage = wrapped_stage
        self.retries = retries

    @property
    def name(self) -> str:
        return (
            f"Retry({self.wrapped_stage.name})"
        )

    def run(
        self,
        context: PipelineContext,
    ) -> None:

        last_error = None

        for attempt in range(
            self.retries + 1
        ):

            try:

                context.metadata[
                    "retry_attempt"
                ] = attempt

                self.wrapped_stage.run(
                    context
                )

                context.metadata[
                    "retry_count"
                ] = attempt

                return

            except RetryableError as exc:

                last_error = exc

                context.metadata[
                    "retry_count"
                ] = attempt + 1

        raise last_error