from pathlib import Path

from .manifest_loader import (
    ManifestLoader,
)


class TagLoader:

    @classmethod
    def load(
        cls,
        tag: str,
    ) -> list[str]:

        matches = []

        for file in ManifestLoader._resolve_path(tag).glob(
            "*.json"
        ):

            manifest = (
                ManifestLoader.load(
                    file.stem
                )
            )

            if tag in manifest.tags:

                matches.append(
                    manifest.name
                )

        return sorted(
            matches
        )
        
    @classmethod
    def list(
        cls,
    ) -> list[str]:

        tags = set()

        for name in (
            ManifestLoader.list()
        ):

            manifest = (
                ManifestLoader.load(
                    name
                )
            )

            tags.update(
                manifest.tags
            )

        return sorted(
            tags
        )

    @classmethod
    def summary(
        cls,
    ) -> dict[str, int]:

        counts = {}

        for name in (
            ManifestLoader.list()
        ):

            manifest = (
                ManifestLoader.load(
                    name
                )
            )

            for tag in manifest.tags:

                counts[tag] = (
                    counts.get(tag, 0)
                    + 1
                )

        return counts