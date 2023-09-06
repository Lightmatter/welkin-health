from pathlib import Path

import tomli

from welkin.__version__ import __version__

pyproject_path = Path(__file__).parent.parent / "pyproject.toml"


def test_version_match():
    with open(pyproject_path, "rb") as f:
        pyproject_toml = tomli.load(f)
        assert pyproject_toml["tool"]["poetry"]["version"] == __version__
