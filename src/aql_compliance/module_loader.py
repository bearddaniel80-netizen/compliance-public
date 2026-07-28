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

def _load_requirements(source, progress, task_id):
    progress.update(
        task_id,
        description="[Install dependencies] ",
    )

    cmd = ["pip", "install", source]
    subprocess.run(
        cmd,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )

    progress.advance(
        task_id
    )

def load(source):
    filename = Path.cwd() / "plugins/module_registry.json"

    with open(filename, "r") as fin:
        raw = json.load(fin)
        
    has_require = source in raw["modules"].keys()
    
    if has_require == False:

        raw["modules"][source] = 1
        
        total_steps = 1

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

            _load_requirements(source, progress, task_id)

            with open(filename, "w") as fout:
                json.dump(raw, fout, indent=2)