import argparse
from dataclasses import dataclass
from pathlib import Path
from subprocess import PIPE, run
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from typing_extensions import Self


@dataclass
class VersionContainingFile:
    name: str
    # Defines how the version in this file will be searched for. Needs to be
    # usable with `git diff -G "<regex>"`
    regex: str


class GitBranch(str):
    pass


def assert_has_diff(path: Path, branch: GitBranch, regex: str) -> None:
    """Assert that there is a git diff that matches the regex in a file"""
    result = run(
        f'git diff --name-only --exit-code -G"{regex}" {branch}',
        stdout=PIPE,
        shell=True,
    )
    relative_path = path.resolve().relative_to(Path.cwd())
    if str(relative_path) not in result.stdout.decode():
        exit(f"Version in [{relative_path}] is stale. Please bump it!")


def cwd_is_a_git_directory() -> bool:
    return Path(".git").exists()


class Parser(argparse.ArgumentParser):
    def __init__(self) -> None:
        super().__init__()
        self.add_argument(
            "--upstream",
            help="Git upstream branch to check the diff against. Default: origin/main",
            default="origin/main",
        )
        self.add_argument(
            "--dirs",
            help="""
            Pipe seperated list of directories to consider source directories. Default:
            src. Example: src|lib
            """,
            default="src",
        )


class Arguments:
    def __init__(self, namespace: argparse.Namespace):
        self._namespace = namespace

    @classmethod
    def from_parser(cls, parser: Parser) -> "Self":
        return cls(parser.parse_args())

    @property
    def upstream(self) -> GitBranch:
        return GitBranch(self._namespace.upstream)

    @property
    def src_directories(self) -> List[str]:
        return self._namespace.dirs.split("|")


class Directories(set):
    @classmethod
    def with_diff_to_branch(cls, branch: GitBranch) -> "Self":
        result = run(
            f"git diff --name-only --exit-code {branch}",
            stdout=PIPE,
            shell=True,
        )
        directories = cls()
        for path in (Path(x) for x in result.stdout.decode().split("\n")):
            directories.update(cls(path.parents))
        return directories


def main() -> None:
    version_containing_files = (
        VersionContainingFile("pyproject.toml", regex=r"^version.*"),
        VersionContainingFile("setup.py", regex=r"^.*version\s*=.*"),
        VersionContainingFile("version.txt", regex=r"^[0-9]*.[0-9]*.*"),
    )

    if not cwd_is_a_git_directory():
        exit("Working directory is not a git directory")

    args = Arguments.from_parser(parser=Parser())

    for directory in Directories.with_diff_to_branch(args.upstream):
        if not any(src_dir in str(directory) for src_dir in args.src_directories):
            continue

        for file in version_containing_files:
            filepath = directory / ".." / file.name
            if filepath.exists():
                assert_has_diff(filepath, branch=args.upstream, regex=file.regex)
