from ..registry import register_execution_plan
from ..virtual import VirtualExecutionPlan

# TODO
# this is placeholder, needs further development
@register_execution_plan("virtual")
class VirtualPlan:

    @classmethod
    def get_plan(cls, context):
        path = context.manifest

        plan = VirtualExecutionPlan(path)

        return plan