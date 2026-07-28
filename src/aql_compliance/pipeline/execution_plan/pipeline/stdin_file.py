from ..registry import register_execution_plan
from ..cat import CatExecutionPlan

@register_execution_plan("stdin_file")
class StdinFilePlan:

    @classmethod
    def get_plan(cls, context):
        path = context.manifest.input.fixture

        plan = CatExecutionPlan(path)

        return plan