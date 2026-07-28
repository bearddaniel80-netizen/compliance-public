from .report_models import ReportContext

class Pipeline:

    def __init__(
        self,
        stages,
    ):

        self.stages = stages

    def run(
        self,
        context: ReportContext,
    ) -> ReportContext:

        for stage in self.stages:

            stage.run(
                context
            )

        return context