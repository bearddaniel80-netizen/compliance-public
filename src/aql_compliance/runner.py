from .pipeline.factory import PipelineFactory
from .models import PipelineConfig, OutputFormat
from .strategies.base import RunnerStrategy
from .strategies.single import ManifestStrategy
from .strategies.suite import SuiteStrategy
from .strategies.tag import TagStrategy
from .execute_context import execute_contexts

def execute_manifest(
    manifest_name,
    fixture_dir,
    _format: OutputFormat,
    profile=False,
    cache=False,
    retry=0,
    fail_fast=False,
    fail_fast_query=False,
):

    config = PipelineConfig(
        fixture_dir=fixture_dir,
        output_format=_format,
        profile=profile,
        cache=cache,
        retry=retry,
        fail_fast=fail_fast,
        fail_fast_query=fail_fast_query,
        parallel=0
    )

    return _run(
        ManifestStrategy(
            manifest_name
        ),
        config,
    )

def execute_suite(
    suite_name: str,
    fixture_dir,
    _format: OutputFormat,
    profile: bool = False,
    cache: bool = False,
    retry: int = 0,
    fail_fast: bool = False,
    fail_fast_query: bool = False,
    parallel: int = 1,
):

    config = PipelineConfig(
        fixture_dir=fixture_dir,
        output_format=_format,
        profile=profile,
        cache=cache,
        retry=retry,
        fail_fast=fail_fast,
        fail_fast_query=fail_fast_query,
        parallel=parallel
    )
    return _run(
        SuiteStrategy(
            suite_name
        ),
        config,
    )

def execute_tag(
    tag_name: str,
    fixture_dir,
    _format: OutputFormat,
    profile: bool = False,
    cache: bool = False,
    retry: int = 0,
    fail_fast: bool = False,
    fail_fast_query: bool = False,
    parallel: int = 1,
):

    config = PipelineConfig(
        fixture_dir=fixture_dir,
        output_format=_format,
        profile=profile,
        cache=cache,
        retry=retry,
        fail_fast=fail_fast,
        fail_fast_query=fail_fast_query,
        parallel=parallel
    )
    return _run(
        TagStrategy(
            tag_name
        ),
        config,
    )


def _run(
    strategy: RunnerStrategy,
    config,
):

    contexts = strategy.build_contexts(
        config
    )

    return execute_contexts(
        contexts,
        config,
    )
