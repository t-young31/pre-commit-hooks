import os
from subprocess import run
from tempfile import TemporaryDirectory

import pytest

from tyhooks import stale_version


def _write_setup_py_file(version: str) -> None:
    with open("setup.py", "w") as file:
        print(f"setup(version='{version}')", file=file)


def test_git_dir_with_diff_exit0(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.argv", ["stale_version.py", "--upstream", "main"])

    with TemporaryDirectory() as tmp_dir:
        os.chdir(tmp_dir)

        run(
            "git init --initial-branch=main && "
            'git config user.name "tmp" && '
            'git config user.email "tmp@example.com"',
            shell=True,
        )
        _write_setup_py_file(version="0.1.0")
        run('git add . && git commit -m "tmp"', shell=True)
        run("git switch -c alt", shell=True)
        run("git branch", shell=True)  # debug info

        os.mkdir("src")
        with open("src/tmp.py", "w") as file:
            print("print('hello world')", file=file)

        run("git add .", shell=True)
        with pytest.raises(SystemExit):  # Not updated the setup file so error
            stale_version.main()

        _write_setup_py_file(version="0.1.1")
        run("git add .", shell=True)
        stale_version.main()  # No error
