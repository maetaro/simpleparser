import subprocess
from typing import List


def run():
    cmds: List[str] = [
        "flake8 simpleparser",
        "mypy simpleparser",
        "pytest",
        "sphinx-apidoc -f -e -o ./docs/source ./",
        "sphinx-build -b html ./docs/source ./docs/build/html"
    ]

    for cmd in cmds:
        result = res = subprocess.run(cmd, shell=True)
        print(result)


if __name__ == '__main__':
    run()