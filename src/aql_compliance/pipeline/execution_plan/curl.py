from .base import ExecutionPlan
from ...models import ExecutionResult

class CurlExecutionPlan(ExecutionPlan):

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
            f'curl -f "{self.raw}" '
            f'| aql query "{query}"'
        )

        return self._run(command)

