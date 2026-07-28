import json

from pathlib import Path

from ..models import (
    Suite,
)


class SuiteLoader:

    @classmethod
    def load(
        cls,
        value: str,
    ) -> Suite:

        path = cls._resolve_path(value) / f"{value}.json"

        data = cls._load_file(path)

        return cls._parse(data)

    @classmethod
    def list(
        cls,
    ) -> list[str]:

        return sorted(
            file.stem
            for file
            in cls._resolve_path("dummy").glob(
                "*.json"
            )
        )

    @classmethod
    def _resolve_path(
        cls,
        value
    ) -> Path:

        path = Path(value)

        if path.exists():
            return path

        return (
            Path.cwd()
            / "suites"
        )

    @classmethod
    def _load_file(
        cls,
        path: Path,
    ) -> dict:

        with open(
            path,
            encoding="utf-8"
        ) as f:
            return json.load(f)

    @classmethod
    def _parse(
        cls,
        data: dict,
    ) -> Suite:

        return Suite(
            name=data["name"],
            manifests=data["manifests"],
        )