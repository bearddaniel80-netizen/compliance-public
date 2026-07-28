from .base import PipelineStage
from ..context import PipelineContext

from ...models import (
    TestResult,
    QueryNode
)

from ...exceptions import (
    FailFastQuery,
)
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
)


class ExecuteStage(
    PipelineStage
):

    @property
    def name(
        self,
    ):
        return "ExecuteStage"

    def run(
        self,
        context: PipelineContext,
    ) -> None:

        context.results = []

        total_queries = (
            self._count_nodes(
                context.tree
            )
        )

        with Progress(
            SpinnerColumn(),
            TextColumn(
                "[progress.description]"
                "{task.description}"
            ),
            BarColumn(),
            TextColumn(
                "{task.completed}"
                "/"
                "{task.total}"
            ),
            TimeElapsedColumn(),
        ) as progress:

            task_id = (
                progress.add_task(
                    "Starting...",
                    total=total_queries,
                )
            )

            self._execute_node(
                node=context.tree,
                context=context,
                progress=progress,
                task_id=task_id,
            )

    def _execute_node(
        self,
        node: QueryNode,
        context,
        progress,
        task_id,
    ) -> None:

        progress.update(
            task_id,
            description=(
                f"[{node.name}] "
                f"{node.query.text}\n"
            ),
        )

        try:

            execution = (
                context.execution_plan
                .execute(
                    node.query.text
                )
            )

            if (
                execution.returncode
                != 0
            ):

                raise RuntimeError(
                    execution.stderr
                )

            context.results.append(
                TestResult(
                    name=node.name,
                    query=node.query,
                    output=execution.stdout,
                    passed=execution.success,
                    error=(
                        execution.stderr
                        if not execution.success
                        else None
                    ),
                    duration_ms=(
                        execution.duration_ms
                    ),
                )
            )

        except Exception as exc:

            context.results.append(
                TestResult(
                    name=node.name,
                    query=node.query,
                    output="",
                    passed=False,
                    error=str(exc),
                    duration_ms=0,
                )
            )

            progress.advance(
                task_id
            )

            if (
                context.fail_fast_query
            ):

                raise FailFastQuery(
                    f"{node.query.text}: "
                    f"{exc}"
                )

            self._skip_children(
                node=node,
                context=context,
                progress=progress,
                task_id=task_id,
            )

            return

        progress.advance(
            task_id
        )

        for child in node.children:

            self._execute_node(
                node=child,
                context=context,
                progress=progress,
                task_id=task_id,
            )

    def _skip_children(
        self,
        node: QueryNode,
        context,
        progress,
        task_id,
    ) -> None:

        for child in node.children:

            context.results.append(
                TestResult(
                    name=child.name,
                    query=child.query,
                    passed=False,
                    skipped=True,
                    output="",
                    error=None,
                    duration_ms=0,
                )
            )

            progress.update(
                task_id,
                description=(
                    f"SKIPPED: "
                    f"{child.query.text}\n"
                ),
            )

            progress.advance(
                task_id
            )

            self._skip_children(
                node=child,
                context=context,
                progress=progress,
                task_id=task_id,
            )

    def _count_nodes(
        self,
        node: QueryNode,
    ) -> int:

        total = 1

        for child in node.children:

            total += (
                self._count_nodes(
                    child
                )
            )

        return total