import json
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import urlopen


def get_json(url):
    """Return decoded JSON, or None for HTTP 404 only."""
    try:
        with urlopen(url, timeout=20) as response:
            return json.load(response)
    except HTTPError as error:
        if error.code == 404:
            return None
        raise


def main():
    path = (
        Path(sys.argv[1]) if len(sys.argv) > 1
        else Path(__file__).with_name("requirements.txt")
    )
    lines = path.read_text(encoding="utf-8").splitlines()
    missing_packages = 0
    missing_versions = 0
    oldest = None

    for number, line in enumerate(lines, start=1):
        name, separator, version = line.strip().partition("==")
        name, version = name.strip(), version.strip()
        if not separator or not name or not version or "==" in version:
            raise ValueError(f"Line {number}: expected package==version")

        base_url = f"https://pypi.org/pypi/{quote(name, safe='')}"
        if get_json(f"{base_url}/json") is None:
            missing_packages += 1
            continue

        release = get_json(f"{base_url}/{quote(version, safe='')}/json")
        if release is None:
            missing_versions += 1
            continue

        if not release["urls"]:
            raise ValueError(f"{name}=={version} exists but has no release files")

        # Follow the assignment: use the first listed file's upload_time.
        upload_time = release["urls"][0]["upload_time"]
        if oldest is None or upload_time < oldest[0]:
            oldest = (upload_time, name, version)

    print(f"Dependencies checked: {len(lines)}")
    print(f"Packages not on PyPI: {missing_packages}")
    print(f"Versions not on PyPI: {missing_versions}")
    if oldest is None:
        print("Oldest pinned release: none")
    else:
        upload_time, name, version = oldest
        print(f"Oldest pinned release: {name}=={version} ({upload_time[:4]})")


if __name__ == "__main__":
    try:
        main()
    except (HTTPError, URLError, TimeoutError, ValueError, OSError, KeyError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
