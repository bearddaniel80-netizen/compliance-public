from pathlib import Path


class FixtureLoader:

    @classmethod
    def load(
        cls,
        fixture_path: str,
    ) -> str:

        return Path(
            fixture_path
        ).read_text(
            encoding="utf-8"
        )