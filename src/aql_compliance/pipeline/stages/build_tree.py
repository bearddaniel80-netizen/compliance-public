from ...generators.tree_generator import TreeGenerator
from .base import PipelineStage
from ..context import PipelineContext

class BuildTreeStage(
    PipelineStage
):

    @property
    def name(self):
        return "BuildTreeStage"

    def run(
        self,
        context: PipelineContext,
    ):
        tree = TreeGenerator()

        context.tree = tree.generate(manifest=context.manifest)