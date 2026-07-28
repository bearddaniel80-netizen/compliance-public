from .base import RunnerStrategy
from ..pipeline.context import PipelineContext

class ManifestStrategy(
    RunnerStrategy
):

    def __init__(
        self,
        manifest_name: str,
    ):
        self.manifest_name = manifest_name


    def build_contexts(
        self,
        config,
    ):

        return [
            PipelineContext(
                manifest_name=self.manifest_name,
                profile=config.profile,
                fail_fast=config.fail_fast,
                fail_fast_query=config.fail_fast_query,
            )
        ]