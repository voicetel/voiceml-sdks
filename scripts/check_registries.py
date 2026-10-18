"""Check advertised package versions using read-only public metadata requests."""

import json
import os
from pathlib import Path
import re
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from xml.etree import ElementTree


def get(url: str, *, missing: bool = False) -> bytes:
    headers = {"User-Agent": "voiceml-catalogue-check"}
    if url.startswith("https://api.github.com/") and os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    try:
        with urlopen(Request(url, headers=headers), timeout=30) as response:
            body = response.read()
    except HTTPError as error:
        if missing and error.code == 404:
            print(f"Expected unpublished package: HTTP 404 {url}")
            return b""
        raise
    if missing:
        raise ValueError("NuGet VoiceML now exists: verify ownership and update the catalogue before recommending it")
    print(f"HTTP 200 {url}")
    return body


def verify(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> None:
    readme = (Path(__file__).resolve().parents[1] / "README.md").read_text()
    version = re.search(r"API-v([\d.]+)-", readme).group(1)
    pypi = json.loads(get(f"https://pypi.org/pypi/voiceml/{version}/json"))
    verify(pypi["info"]["version"] == version, "PyPI version mismatch")
    npm = json.loads(get(f"https://registry.npmjs.org/@voicetel.com%2fvoiceml/{version}"))
    verify(npm["name"] == "@voicetel.com/voiceml" and npm["version"] == version, "npm identity/version mismatch")
    go = json.loads(get(f"https://proxy.golang.org/github.com/voicetel/voiceml-go-sdk/@v/v{version}.info"))
    verify(go["Version"] == f"v{version}", "Go proxy version mismatch")
    pom = ElementTree.fromstring(get(f"https://repo.maven.apache.org/maven2/com/voicetel/voiceml/{version}/voiceml-{version}.pom"))
    verify(pom.findtext("{*}version") == version, "Maven version mismatch")
    ruby = json.loads(get(f"https://rubygems.org/api/v2/rubygems/voiceml/versions/{version}.json"))
    verify(ruby["version"] == version, "RubyGems version mismatch")
    php = json.loads(get("https://repo.packagist.org/p2/voicetel/voiceml.json"))
    verify(any(package["version"].removeprefix("v") == version for package in php["packages"]["voicetel/voiceml"]), "Packagist version missing")
    swift = json.loads(get(f"https://api.github.com/repos/voicetel/voiceml-swift/git/ref/tags/v{version}"))
    verify(swift["ref"] == f"refs/tags/v{version}", "Swift tag missing")
    get("https://api.nuget.org/v3-flatcontainer/voiceml/index.json", missing=True)

    releases = re.findall(r"https://github.com/(voicetel/[^/]+)/releases/tag/(v[\d.]+)", readme)
    for repo, tag in sorted(set(releases)):
        release = json.loads(get(f"https://api.github.com/repos/{repo}/releases/tags/{tag}"))
        verify(release["tag_name"] == tag and not release["draft"] and not release["prerelease"], f"Release unavailable: {repo} {tag}")
    print("Advertised registry versions and GitHub Releases verified; NuGet absence remains explicit.")


if __name__ == "__main__":
    main()
