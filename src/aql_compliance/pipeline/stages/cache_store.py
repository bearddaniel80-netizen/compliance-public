from .base import PipelineStage
from ..context import PipelineContext
from dataclasses import asdict
import json


class StoreCacheStage(
    PipelineStage
):

    @property
    def name(self):
        return "StoreCacheStage"

    def run(
        self,
        context: PipelineContext,
    ) -> None:

        if context.metadata.get(
            "cache_hit"
        ):
            return

        cache_file = context.metadata[
            "cache_file"
        ]

        payload = [
            asdict(r)
            for r in context.results
        ]

        cache_file.write_text(
            json.dumps(
                payload,
                indent=2,
            ),
            encoding="utf-8",
        )