from .base import RunnerStrategy
from ..loaders.suite_loader import SuiteLoader
from ..pipeline.context import PipelineContext

class SuiteStrategy(
    RunnerStrategy
):

    def __init__(
        self,
        suite_name,
    ):
        self.suite_name = suite_name

    def build_contexts(
        self,
        config,
    ):

        suite = SuiteLoader.load(
            self.suite_name
        )

        return [
            PipelineContext(
                manifest_name=name,
                profile=config.profile,
                fail_fast=config.fail_fast,
                fail_fast_query=config.fail_fast_query,
            )
            for name in suite.manifests
        ]