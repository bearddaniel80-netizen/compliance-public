import hashlib
import json
from pathlib import Path

from .base import PipelineStage
from ..context import PipelineContext


class CacheStage(PipelineStage):

    def __init__(
        self,
        cache_dir: str = ".aql-test-cache",
    ):
        self.cache_dir = Path.cwd() / cache_dir

        self.cache_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    @property
    def name(self):
        return "CacheStage"

    def run(
        self,
        context: PipelineContext,
    ) -> None:

        cache_key = self._build_key(
            context
        )

        cache_file = (
            self.cache_dir
            / f"{cache_key}.json"
        )

        context.metadata[
            "cache_key"
        ] = cache_key

        context.metadata[
            "cache_file"
        ] = cache_file

        if cache_file.exists():

            context.metadata[
                "cache_hit"
            ] = True

            context.metadata[
                "cached_results"
            ] = json.loads(
                cache_file.read_text(
                    encoding="utf-8"
                )
            )

        else:

            context.metadata[
                "cache_hit"
            ] = False

    def _build_key(
        self,
        context,
    ) -> str:

        payload = {
            "manifest": context.manifest_name,
            "fixture": context.fixture_data,
        }

        return hashlib.sha256(
            json.dumps(
                payload,
                sort_keys=True,
            ).encode()
        ).hexdigest()