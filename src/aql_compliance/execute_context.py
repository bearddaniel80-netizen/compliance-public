from .pipeline.context import PipelineContext
from .pipeline.factory import PipelineFactory
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)

def execute_contexts(
    contexts: list[PipelineContext],
    config,
) -> list[PipelineContext]:
    if config.parallel <= 1:
        return _sequential(config, contexts)
    
    return _parallel(config, contexts)

def _sequential(config, contexts):

    completed = []

    #
    # Sequential
    #

    for context in contexts:

        context = _execute_context(
            context,
            config,
        )

        completed.append(
            context
        )

        if config.fail_fast:

            failed = any(
                not result.passed
                and not result.skipped
                for result in context.results
            )

            if failed:
                break

    return completed

def _parallel(config, contexts):
    #
    # Parallel
    #
    completed = []

    with ThreadPoolExecutor(
        max_workers=config.parallel,
    ) as executor:

        futures = [

            executor.submit(
                _execute_context,
                context,
                config,
            )

            for context in contexts
        ]

        for future in as_completed(
            futures
        ):

            completed.append(
                future.result()
            )

    return completed


def _execute_context(
    context,
    config,
):

    pipeline = PipelineFactory(
        config=config,
        context=context,
    ).build()

    return pipeline.run(
        context
    )

