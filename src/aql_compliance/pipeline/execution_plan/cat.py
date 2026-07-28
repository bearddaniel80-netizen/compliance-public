from .base import ExecutionPlan
from ...models import ExecutionResult

class CatExecutionPlan(
    ExecutionPlan
):

    def __init__(
        self,
        file_path: str,
    ):
        self.file_path = file_path

    def execute(
        self,
        query: str,
    ) -> ExecutionResult:

        command = (
            f'cat "{self.file_path}" '
            f'| aql query "{query}"'
        )

        return self._run(command)