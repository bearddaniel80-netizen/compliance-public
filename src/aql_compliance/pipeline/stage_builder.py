class CompliancePipeline:

    def __init__(
        self,
        *stages,
    ):
        self.stages = stages

    def run(
        self,
        context,
    ):

        for stage in self.stages:

            stage.run(
                context
            )

            if context.metadata.get(
                "pipeline_stop"
            ):
                break
                
        return context