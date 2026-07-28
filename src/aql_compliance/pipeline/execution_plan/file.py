from .base import ExecutionPlan
from ...models import ExecutionResult
from pathlib import Path

class FileExecutionPlan(
    ExecutionPlan
):

    def __init__(
        self,
        source,
        file_path: str,
    ):
        self.source = source
        self.file_path = Path.cwd() / file_path

    def execute(
        self,
        query: str,
    ) -> ExecutionResult:

        query = query.replace(
            "source", f"{self.source}({self.file_path})"
        )

        command = (
            f'aql query "{query}"'
        )

        return self._run(command)