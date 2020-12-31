"""check and doc build utility."""

import subprocess
from typing import List


def run() -> None:
    """Run check utils."""
    cmds: List[str] = [
        "flake8 simpleparser --count --select=E9,F63,F7,F82 --show-source --statistics",
        "flake8 simpleparser --count --max-complexity=10 --max-line-length=127 --statistics",
        "mypy .",
        "pytest",
        "sphinx-apidoc -f -e -o ./docs/source ./",
        "sphinx-build -b html ./docs/source ./docs/build/html"
    ]

    for cmd in cmds:
        result = subprocess.run(cmd, shell=True)
        print(result)
        if result.returncode != 0:
            return


if __name__ == '__main__':
    run()
