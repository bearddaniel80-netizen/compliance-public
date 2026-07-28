import typer

from .commands.manifest import (
    app as manifest_app,
)

from .commands.suite import (
    app as suite_app,
)

from .commands.tag import (
    app as tag_app,
)

app = typer.Typer(
    help="AQL Compliance Test Framework"
)

app.add_typer(
    manifest_app,
    name="manifest",
)

app.add_typer(
    suite_app,
    name="suite",
)

app.add_typer(
    tag_app,
    name="tag",
)