import typer
from pathlib import Path

from ..exceptions import FailFastQuery
from ..models import OutputFormat
from ..runner import execute_suite
from ..loaders.suite_loader import SuiteLoader

app = typer.Typer()

@app.command()
def run(
    suite_name: str= typer.Argument(
        ...,
        help="Suite name or path",
    ),
    cache: bool = typer.Option(
        False,
        "--cache",
        help="Enable result caching",
    ),
    _format: OutputFormat = typer.Option(
        OutputFormat.RICH,
        "--format",
        help="Output format"
    ),
    fail_fast: bool = typer.Option(
        False,
        "--fail-fast",
        help="Stop on first failure",
    ),
    fail_fast_query: bool = typer.Option(
        False,
        "--fail-fast-query",
        help="Stop on first failing query",
    ),
    fixture_dir: Path = typer.Option(
        "./fixtures"
    ),
    parallel: int = typer.Option(
        1,
        "--parallel",
        "-p",
        help="Number of manifests to execute concurrently",
    ),
    profile: bool = typer.Option(
        False,
        "--profile",
        help="Display execution timings",
    ),
    retry: int = typer.Option(
        0,
        "--retry",
        help="Number of retries",
    ),
):

    try:
        context = execute_suite(
            suite_name,
            fixture_dir,
            _format,
            profile,
            cache,
            retry,
            fail_fast,
            fail_fast_query,
            parallel,
        )
    
    except FailFastQuery as exc:

        typer.secho(
            f"\nFAIL-FAST-QUERY: {exc}",
            fg=typer.colors.RED,
        )

        raise typer.Exit(1)

@app.command("list")
def list_suites():

    suites = (
        SuiteLoader.list()
    )

    for suite in suites:
        print(suite)