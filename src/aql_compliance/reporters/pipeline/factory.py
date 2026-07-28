from .pipeline import Pipeline

from .stages.collect import CollectStage
from .stages.metrics import MetricsStage
from .stages.render import RenderStage
from .stages.write import WriteStage
from .stages.browser import OpenBrowserStage

from .report_models import ReportContext
from .report_factory import ReporterFactory

from ...models import (
    OutputFormat,
)


class ReportPipelineFactory:

    @classmethod
    def create(
        cls,
        report_context: ReportContext,
        open_browser: bool = False,
    ) -> Pipeline:

        renderer, writer = (
            ReporterFactory.build(
                report_context.output_format
            )
        )

        stages = [

            CollectStage(),
            MetricsStage(),

            RenderStage(
                renderer
            ),

            WriteStage(
                writer
            ),
        ]

        if (
            report_context.output_format
            == OutputFormat.HTML
            and open_browser
        ):

            stages.append(
                OpenBrowserStage()
            )

        return Pipeline(
            stages
        )