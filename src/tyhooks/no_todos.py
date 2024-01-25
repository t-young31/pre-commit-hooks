import re
from argparse import ArgumentParser

PATTERN = r"^.*[#|//]\s*TODO.*$"


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("filename", nargs="+")
    args = parser.parse_args()

    for filename in args.filename:
        content = open(filename).read()
        matches = re.findall(PATTERN, content, flags=re.MULTILINE | re.IGNORECASE)
        if len(matches) > 0:
            exit(f"Found TODO in {filename}\n\n" + "\n".join(matches))
