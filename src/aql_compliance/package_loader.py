import json
import subprocess
from pathlib import Path
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
)

def _install_package(raw, source, progress, task_id):
    progress.update(
        task_id,
        description="[Install wheel] ",
    )

    _path = Path.cwd() / raw["plugins"][source]["path"]

    wheel = next((_path / "dist").glob("*.whl"))

    subprocess.run(
        ["pip", "install", "--force-reinstall", str(wheel)],
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )

    progress.advance(
        task_id
    )

def _create_package(raw, source, progress, task_id):
    progress.update(
        task_id,
        description="[Build wheel] ",
    )

    _path = Path.cwd() / raw["plugins"][source]["path"]
    subprocess.run(
        ["python", "-m", "build"],
        cwd=_path,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )

    progress.advance(
        task_id
    )

def _load_requirements(raw, source, progress, task_id):
    progress.update(
        task_id,
        description="[Install dependencies] ",
    )

    _path = Path.cwd() / raw["plugins"][source]["path"]
    cmd = ["pip", "install", "-r", "requirements.txt"]
    subprocess.run(
        cmd,
        cwd=_path,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )

    progress.advance(
        task_id
    )

def load(source):
    filename = Path.cwd() / "plugins/package_registry.json"

    with open(filename, "r") as fin:
        raw = json.load(fin)

    if raw["plugins"][source]["loaded"] == False:

        raw["plugins"][source]["loaded"] = True
        
        has_require = "require" in raw["plugins"][source].keys()
        
        total_steps = 3 if has_require else 2

        with Progress(
            SpinnerColumn(),
            TextColumn(
                "[progress.description]"
                "{task.description}"
            ),
            BarColumn(),
            TextColumn(
                "{task.completed}"
                "/"
                "{task.total}"
            ),
            TimeElapsedColumn(),
        ) as progress:

            task_id = (
                progress.add_task(
                    "Starting...",
                    total=total_steps,
                )
            )

            if has_require == True:
                _load_requirements(raw, source, progress, task_id)
            
            _create_package(raw, source, progress, task_id)

            _install_package(raw, source, progress, task_id)

            with open(filename, "w") as fout:
                json.dump(raw, fout, indent=2)