import os
from tempfile import TemporaryDirectory

import pytest

from tyhooks import no_todos


def test_no_todo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.argv", ["no_todos.py", "tmp.py"])

    with TemporaryDirectory() as tmp_dir:
        os.chdir(tmp_dir)

        with open("tmp.py", "w") as file:
            print("print('hello world')", file=file)

        no_todos.main()  # No error


def test_divide_by_todo(monkeypatch: pytest.MonkeyPatch) -> None:
    """Checks that divisions are not confused with single-line comments"""
    monkeypatch.setattr("sys.argv", ["no_todos.py", "tmp.py"])

    with TemporaryDirectory() as tmp_dir:
        os.chdir(tmp_dir)

        with open("tmp.py", "w") as file:
            print(
                """
            todo = 1
            done = 10 / todo
            """,
                file=file,
            )

        no_todos.main()  # No error


def test_empty_comment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Checks that empty comments do not get flagged"""
    monkeypatch.setattr("sys.argv", ["no_todos.py", "tmp.py"])

    with TemporaryDirectory() as tmp_dir:
        os.chdir(tmp_dir)

        with open("tmp.py", "w") as file:
            print("print('hello world') #", file=file)

        no_todos.main()  # No error


def test_has_todo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.argv", ["no_todos.py", "tmp.py"])

    with TemporaryDirectory() as tmp_dir:
        os.chdir(tmp_dir)

        with open("tmp.py", "w") as file:
            print("print('hello world') # TODO: update", file=file)

        with pytest.raises(SystemExit):  # Not updated the setup file so error
            no_todos.main()
