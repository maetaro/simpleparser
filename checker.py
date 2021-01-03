"""check and doc build utility."""

import subprocess
from typing import List


def run() -> None:
    """Run check utils."""
    cmds: List[str] = [
        "flake8 simpleparser test demo --count --select=E9,F63,F7,F82 --show-source --statistics",  # noqa E501
        "flake8 simpleparser test demo --count --max-complexity=10 --max-line-length=127 --statistics",  # noqa E501
        "mypy .",
        "pytest",
        "coverage xml",
        "sphinx-apidoc -f -e -o ./doc/source ./",
        "sphinx-build -b html ./doc/source ./doc/build/html"
    ]

    for cmd in cmds:
        result = subprocess.run(cmd, shell=True)
        if result.returncode != 0:
            print(result)
            return


if __name__ == '__main__':
    run()
