from .base import PipelineStage
from ..context import PipelineContext
from ...models import SourceType

class QueryResolverStage(
    PipelineStage
):

    def run(
        self,
        context: PipelineContext,
    ):
        source = (
            self._resolve_source(
                context
            )
        )

        self._resolve_node(
            context.tree,
            source,
        )

        return context

    @property
    def name(self):
        return "QueryResolverStage"

    def _resolve_source(
        self,
        context,
    ):

        input_type = (
            context.manifest.input.type
        )

        if input_type.startswith(
            "stdin"
        ):
            return "stdin"

        return (
            f"{context.manifest.input.source}"
            f"('{context.manifest.input.fixture}')"
        )

    def _resolve_node(
        self,
        node,
        source: str,
    ):

        node.query.text = (
            node.query.text.replace(
                "source",
                source,
            )
        )

        for child in node.children:

            self._resolve_node(
                child,
                source,
            )