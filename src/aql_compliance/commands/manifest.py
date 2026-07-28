import typer
from pathlib import Path

from ..exceptions import FailFastQuery
from ..models import OutputFormat
from ..runner import execute_manifest
from ..loaders.manifest_loader import ManifestLoader

app = typer.Typer()

@app.command()
def run(
    manifest_name: str = typer.Argument(
        ...,
        help="Manifest name or path",
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
    ),
    fail_fast_query: bool = typer.Option(
        False,
        "--fail-fast-query",
        help="Stop on first failing query",
    ),
    fixture_dir: Path = typer.Option(
        "./fixtures",
        help="Fixture directory",
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
    """
    Run a single manifest.
    """

    try:
        context = execute_manifest(
            manifest_name,
            fixture_dir,
            _format,
            profile,
            cache,
            retry,
            fail_fast,
            fail_fast_query,
        )

    except FailFastQuery as exc:

        typer.secho(
            f"\nFAIL-FAST-QUERY: {exc}",
            fg=typer.colors.RED,
        )

        raise typer.Exit(1)

@app.command("list")
def list_manifests():

    manifests = (
        ManifestLoader.list()
    )

    for manifest in manifests:
        typer.echo(manifest)
        typer.echo()