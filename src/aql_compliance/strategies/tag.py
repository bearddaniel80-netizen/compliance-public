
from ..pipeline.context import PipelineContext
from ..loaders.tag_loader import TagLoader
from .base import RunnerStrategy

class TagStrategy(
    RunnerStrategy
):

    def __init__(
        self,
        tag: str,
    ):
        self.tag = tag

    def build_contexts(
        self,
        config,
    ):

        manifests = TagLoader.load(
            self.tag
        )

        return [
            PipelineContext(
                manifest_name=name,
                profile=config.profile,
                fail_fast=config.fail_fast,
                fail_fast_query=config.fail_fast_query,
            )
            for manifest in manifests
        ]