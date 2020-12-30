"""check and doc build utility."""

import subprocess
from typing import List


def run() -> None:
    """main function."""
    cmds: List[str] = [
        "flake8 simpleparser",
        "mypy .",
        "pytest",
        "sphinx-apidoc -f -e -o ./docs/source ./",
        "sphinx-build -b html ./docs/source ./docs/build/html"
    ]

    for cmd in cmds:
        result = subprocess.run(cmd, shell=True)
        print(result)


if __name__ == '__main__':
    run()
