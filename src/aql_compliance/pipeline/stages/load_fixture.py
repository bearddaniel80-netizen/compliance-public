from ...loaders.fixture_loader import FixtureLoader
from .base import PipelineStage
from ..context import PipelineContext

from pathlib import Path

class LoadFixtureStage(
    PipelineStage
):

    def __init__(
        self,
        fixture_dir,
    ):
        self.fixture_dir = Path(
            fixture_dir
        )

    @property
    def name(self):
        return "LoadFixtureStage"

    def run(
        self,
        context: PipelineContext,
    ):

        fixture_path = (
            self.fixture_dir
            / context.manifest.input.fixture
        )

        context.fixture_data = (
            FixtureLoader.load(
                fixture_path
            )
        )