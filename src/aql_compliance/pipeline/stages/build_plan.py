from .base import PipelineStage
from ..context import PipelineContext
from ..execution_plan import pipeline
from ..execution_plan.registry import EXECUTE_PLAN_REGISTRY

class BuildExecutionPlanStage(
    PipelineStage
):

    @property
    def name(self):
        return "BuildExecutionPlanStage"

    def run(
        self,
        context: PipelineContext,
    ):

        input_type = (
            context.manifest.input.type
        )
        
        plan = EXECUTE_PLAN_REGISTRY[input_type]
        
        if plan is not None:

            context.execution_plan = plan.get_plan(context)

        else:

            raise ValueError(
                f"Unknown input type "
                f"{input_type}"
            )