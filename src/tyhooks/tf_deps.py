import argparse
import re
from datetime import date as Date
from datetime import timedelta
from enum import Enum


class Frequency(Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"

    def __str__(self) -> str:
        return self.value


class Parser(argparse.ArgumentParser):
    def __init__(self) -> None:
        super().__init__()
        self.add_argument("filename", nargs="+")
        self.add_argument(
            "--frequency",
            help="Frequency at which comment updates are required",
            default="weekly",
            choices=list(Frequency),
        )


class Arguments:
    def __init__(self) -> None:
        self._namespace = Parser().parse_args()

    @property
    def frequency(self) -> Frequency:
        return Frequency[self._namespace.frequency]

    @property
    def tf_filenames(self) -> list[str]:
        return [f for f in self._namespace.filename if f.endswith(".tf")]


class Resource:
    def __init__(self, hcl_block: list[str]):
        assert len(hcl_block) > 0
        self._hcl_block = hcl_block

    @property
    def name(self) -> str:
        assert "resource" in self._hcl_block[0]
        match = re.findall(r"resource \"?(\w+)\"? \"?(\w+)\"?", self._hcl_block[0])
        if len(match) < 1:
            return "???"
        else:
            resource_type, resource_name = match[0]
            return f"{resource_type}.{resource_name}"

    def version_checked_after(self, date: Date) -> bool:
        try:
            line = next(
                line for line in self._hcl_block if line.lstrip().startswith("version")
            )
        except StopIteration:  # no version
            return True

        if "checked" not in line:
            return False

        match = re.findall(
            pattern=r".*(#|/{2}.*)\s*checked\s*(\d{4})[-|:](\d{1,2})[-|:](\d{1,2})",
            string=line,
        )
        if len(match) == 0:
            exit(f"Failed to match on: {line}")

        _, year, month, day = match[0]
        return Date(year=int(year), month=int(month), day=int(day)) > date


class File:
    def __init__(self, content: str):
        self._content = content

    @property
    def resources(self) -> list[Resource]:
        resources: list[Resource] = []
        block = []
        for line in self._content.split("\n"):
            if line.startswith("resource"):
                block = [line]
            if line.startswith("}") and block != []:
                resources.append(Resource(block))
            if block != [] and line.strip() != "":
                block.append(line)

        return resources


def last_allowable_date_from_frequency(frequency: Frequency) -> Date:
    last_allowable_date = Date.today()
    if frequency == Frequency.daily:
        last_allowable_date -= timedelta(days=1)
    elif frequency == Frequency.weekly:
        last_allowable_date -= timedelta(days=7)
    elif frequency == Frequency.monthly:
        last_allowable_date -= timedelta(days=30)

    return last_allowable_date


def main() -> None:
    args = Arguments()
    date = last_allowable_date_from_frequency(args.frequency)

    for filename in args.tf_filenames:
        content = open(filename, "r").read()
        if "version" not in content:
            continue
        for resource in File(content).resources:
            if not resource.version_checked_after(date):
                exit(
                    f"The version of [{resource.name}] was not checked recently enough. "
                    f"Either add a comment to the version line in the form "
                    f"[# checked {Date.today()}]. Needed >{date}"
                )


if __name__ == "__main__":
    main()
