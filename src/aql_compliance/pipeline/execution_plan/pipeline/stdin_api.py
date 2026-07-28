from ..registry import register_execution_plan
from ..curl import CurlExecutionPlan

# TODO
# this is placeholder, needs further development
@register_execution_plan("stdin_api")
class StdinApiPlan:

    @classmethod
    def get_plan(cls, context):
        path = context.fixture_data

        plan = CurlExecutionPlan(path)

        return plan