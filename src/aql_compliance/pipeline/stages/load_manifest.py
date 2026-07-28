from ...loaders.manifest_loader import ManifestLoader
from .base import PipelineStage
from ..context import PipelineContext

class LoadManifestStage(
    PipelineStage
):

    @property
    def name(self):
        return "LoadManifestStage"

    def run(
        self,
        context: PipelineContext,
    ):

        context.manifest = (
            ManifestLoader.load(
                context.manifest_name
            )
        )