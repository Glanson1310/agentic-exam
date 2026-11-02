import json
import sys
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import urlopen
from packaging.specifiers import SpecifierSet
from packaging.version import Version


def get_release(name, version):
    url = f"https://pypi.org/pypi/{quote(name, safe='')}/{quote(version, safe='')}/json"
    try:
        with urlopen(url, timeout=30) as response:
            return json.load(response)
    except HTTPError as error:
        if error.code == 404:
            return None
        raise


def minimum_bound(specifiers):
    # Compare declared lower bounds numerically, including compound constraints.
    bounds = []
    for spec in specifiers:
        if spec.operator in (">=", ">", "~=", "==", "==="):
            bounds.append(Version(spec.version.removesuffix(".*")))
    return max(bounds) if bounds else None


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("requirements.txt")
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    missing = incompatible = 0
    highest = None
    for number, line in enumerate(lines, 1):
        name, separator, version = line.strip().partition("==")
        name, version = name.strip(), version.strip()
        if not separator or not name or not version:
            raise ValueError(f"Line {number}: expected name==version")
        release = get_release(name, version)
        if release is None:
            missing += 1
            continue
        requirement = release["info"].get("requires_python") or ""
        specs = SpecifierSet(requirement)
        if not specs.contains("3.11"):
            incompatible += 1
        bound = minimum_bound(specs)
        if bound is not None and (highest is None or bound > highest[0]):
            highest = (bound, name, version)
    print(f"Dependencies checked: {len(lines)}")
    print(f"Not found on PyPI: {missing}")
    print(f"Incompatible with Python 3.11: {incompatible}")
    if highest:
        bound, name, version = highest
        print(f"Highest requirement: {name}=={version} (>={bound})")
    else:
        print("Highest requirement: none")


if __name__ == "__main__":
    main()
