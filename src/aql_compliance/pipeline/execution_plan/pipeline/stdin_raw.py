from ..registry import register_execution_plan
from ..echo import EchoExecutionPlan

@register_execution_plan("stdin_raw")
class StdinRawPlan:

    @classmethod
    def get_plan(cls, context):
        path = context.fixture_data

        plan = EchoExecutionPlan(path)

        return plan