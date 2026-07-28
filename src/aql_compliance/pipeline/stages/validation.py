from .base import PipelineStage
from ..context import PipelineContext
from ...validators import (
    validate,
)
from ...exceptions import (
    ValidationError,
)


class ValidateStage(
    PipelineStage
):

    @property
    def name(self):
        return "ValidateStage"

    def run(
        self,
        context: PipelineContext,
    ) -> None:

        for result in context.results:

            if result.skipped:
                continue

            if not result.passed:
                continue

            try:

                validate(
                    query=result.query,
                    output=result.output,
                    manifest=context.manifest,
                )

            except ValidationError as exc:

                result.passed = False

                result.error = str(exc)

                if context.fail_fast_query:
                    raise