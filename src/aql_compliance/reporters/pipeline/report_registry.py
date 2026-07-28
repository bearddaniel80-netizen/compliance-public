from ...models import OutputFormat
from .report_models import ReporterRole
from collections.abc import Iterable

REPORTERS = {}

def reporter(
    formats,
    role,
):
    if not isinstance(formats, Iterable):
        formats = [formats]

    def decorator(cls):
        for output_format in formats:
            REPORTERS.setdefault(
                output_format,
                {}
            )
            REPORTERS[output_format][role] = cls

        return cls

    return decorator