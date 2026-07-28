from .stage_builder import CompliancePipeline
from .context import PipelineContext
from .stages.load_manifest import LoadManifestStage
from .stages.load_fixture import LoadFixtureStage
from .stages.cache import CacheStage
from .stages.cache_bypass import CacheBypassStage
from .stages.cache_store import StoreCacheStage
from .stages.build_tree import BuildTreeStage
from .stages.build_plan import BuildExecutionPlanStage
from .stages.retry import RetryStage
from .stages.profile import ProfileStage
from .stages.execute import ExecuteStage
from .stages.report import ReportStage
from .stages.metrics import MetricsStage
from .stages.validation import ValidateStage
from .stages.query_resolver import QueryResolverStage

class PipelineFactory:

    def __init__(
        self,
        config,
        context,
    ):
        self.context = context

        self.fixture_dir = config.fixture_dir

        self.output_format = config.output_format

        self.cache = config.cache

        self.retry = config.retry

        self.profile = config.profile

    def build(
        self,
    ) -> CompliancePipeline:

        stages = []

        stages.append(
            self._profile(
                LoadManifestStage()
            )
        )

        stages.append(
            self._profile(
                LoadFixtureStage(
                    fixture_dir=self.fixture_dir,
                )
            )
        )

        if self.cache:

            stages.append(
                self._profile(
                    CacheStage()
                )
            )

            stages.append(
                self._profile(
                    CacheBypassStage()
                )
            )

        stages.append(
            self._profile(
                BuildTreeStage()
            )
        )

        stages.append(
            self._profile(
                QueryResolverStage()
            )
        )
        
        stages.append(
            self._profile(
                BuildExecutionPlanStage()
            )
        )

        execute_stage = ExecuteStage()

        if self.retry > 0:

            execute_stage = RetryStage(
                execute_stage,
                retries=self.retry,
            )

        stages.append(
            self._profile(
                execute_stage
            )
        )

        stages.append(
            self._profile(
                ValidateStage()
            )
        )

        if self.cache:

            stages.append(
                self._profile(
                    StoreCacheStage()
                )
            )

        stages.append(MetricsStage())

        stages.append(
            self._profile(
                ReportStage(
                    output_format=self.output_format,
                )
            )
        )

        return CompliancePipeline(
            *stages
        )

    def _profile(
        self,
        stage,
    ):

        if not self.profile:
            return stage

        return ProfileStage(
            stage
        )