import json

from pathlib import Path

from ..models import (
    Manifest,
    InputConfig,
    AssertionConfig,
)


class ManifestLoader:

    @classmethod
    def load(
        cls,
        value: str,
    ) -> Manifest:
        
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
            / "manifests"
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
    ) -> Manifest:

        return Manifest(
            name=data["name"],

            input=InputConfig(
                type=data["input"]["type"],
                fixture=data["input"]["fixture"],
                source=data["input"]["source"]
            ),

            fields=data["fields"],

            filters=data["filters"],

            assertions=AssertionConfig(
                min_rows=data
                    .get("assertions", {})
                    .get("min_rows", 1),

                required_fields=data
                    .get("assertions", {})
                    .get(
                        "required_fields",
                        []
                    ),
            ),

            tags=data.get("tags", []),
        )