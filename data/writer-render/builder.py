#!/usr/bin/env python3

import json
from pathlib import Path
from textwrap import dedent


PYPROJECT_TEMPLATE = """\
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "aql_{plugin}"
version = "0.0.1"
description = "AQL Plugin"
authors = [{{ name = "Daniel Beard" }}]
requires-python = ">=3.10"

[tool.setuptools]
package-dir = {{"" = "src"}}

[tool.setuptools.packages.find]
where = ["src"]
"""


def create_plugin(plugin_name: str, config: dict):
    plugin_root = Path("plugins") / plugin_name
    package_dir = plugin_root / "src" / f"aql_{plugin_name}" / "adaptor"

    # Create directory tree
    package_dir.mkdir(parents=True, exist_ok=True)

    # Create __init__.py
    (package_dir / "__init__.py").touch(exist_ok=True)

    # Create source.py
    (package_dir / f"{plugin_name}_source.py").touch(exist_ok=True)

    # Create pyproject.toml
    pyproject = plugin_root / "pyproject.toml"
    pyproject.write_text(
        PYPROJECT_TEMPLATE.format(plugin=plugin_name),
        encoding="utf-8",
    )

    # Create requirements.txt if needed
    requirements = config.get("require")
    if requirements:
        req_file = plugin_root / "requirements.txt"
        req_file.write_text(
            "\n".join(requirements) + "\n",
            encoding="utf-8",
        )

    print(f"Created {plugin_root}")


def walk_plugins(data):
    """
    Recursively walk the JSON looking for plugin definitions.
    A plugin definition is any dict containing a 'path' key.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                if "path" in value:
                    create_plugin(key, value)
                else:
                    walk_plugins(value)

    elif isinstance(data, list):
        for item in data:
            walk_plugins(item)


def main():
    json_file = Path("package_registry.json")

    with json_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    walk_plugins(data)


if __name__ == "__main__":
    main()