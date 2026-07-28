from .base import ExecutionPlan
from ...models import ExecutionResult

class EchoExecutionPlan(ExecutionPlan):

    def __init__(
        self,
        raw: str,
    ):
        self.raw = raw

    def execute(
        self,
        query: str,
    ) -> ExecutionResult:

        command = (
            f'echo "{self.raw}" '
            f'| aql query "{query}"'
        )

        return self._run(command)

