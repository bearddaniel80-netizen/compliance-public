from abc import ABC
from abc import abstractmethod
import subprocess
import time

from ...models import ExecutionResult

class ExecutionPlan(ABC):

    @abstractmethod
    def execute(
        self,
        query: str,
    ) -> ExecutionResult:
        pass

    def _run(self, command):
        start = time.perf_counter()

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
        )

        duration_ms = int(
            (
                time.perf_counter()
                - start
            ) * 1000
        )

        return ExecutionResult(
            command=command,
            stdout=result.stdout,
            stderr=result.stderr,
            returncode=result.returncode,
            duration_ms=duration_ms,
        )