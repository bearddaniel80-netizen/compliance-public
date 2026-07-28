from ...models import (
    OutputFormat,
)
from .report_models import ReporterRole
from .report_registry import REPORTERS

from . import renderers
from . import writers

class ReporterFactory:

    @classmethod
    def build(
        cls,
        output_format,
    ):
        renderer = (
            cls._lookup(
                output_format,
                ReporterRole.RENDERER
            )
        )

        writer = (
            cls._lookup(
                output_format,
                ReporterRole.WRITER
            )
        )
        
        if renderer is None or writer is None:
            raise RuntimeError(list(REPORTERS.keys())[:2])

        return (
            renderer,
            writer,
        )

    @classmethod
    def _lookup(
        cls,
        output_format,
        reporter_type,
    ):
        return (
            REPORTERS
            .get(output_format, {})
            .get(reporter_type)
        )