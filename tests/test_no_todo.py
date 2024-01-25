import os
from tempfile import TemporaryDirectory

import pytest

from tyhooks import no_todos


def test_no_todo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.argv", ["no_todos.py", "tmp.py"])

    with TemporaryDirectory() as tmp_dir:
        os.chdir(tmp_dir)

        with open("tmp.py", "w") as file:
            print("print('hello world') # TODO: update", file=file)

        with pytest.raises(SystemExit):  # Not updated the setup file so error
            no_todos.main()

        with open("tmp.py", "w") as file:
            print("print('hello world')", file=file)

        no_todos.main()  # No error
