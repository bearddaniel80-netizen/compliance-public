from ..registry import register_execution_plan
from ..file import FileExecutionPlan

@register_execution_plan("file")
class FilePlan:

    @classmethod
    def get_plan(cls,  context):
        source = context.manifest.input.source
        path = context.manifest.input.fixture

        plan = FileExecutionPlan(source, path)

        return plan