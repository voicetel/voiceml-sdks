"""Read-only preflight for a coordinated release of the official SDKs."""

import argparse
import base64
import json
import re
import sys

from check_registries import get


SDK_VERSIONS = {
    "voiceml-python-sdk": ("pyproject.toml", "src/voiceml/_version.py"),
    "voiceml-node-sdk": ("package.json", "package-lock.json", "src/version.ts"),
    "voiceml-go-sdk": ("version.go",),
    "voiceml-java-sdk": ("pom.xml", "src/main/java/com/voicetel/voiceml/Version.java"),
    "voiceml-csharp-sdk": ("src/VoiceML/VoiceML.csproj", "src/VoiceML/Version.cs"),
    "voiceml-ruby-sdk": ("lib/voiceml/version.rb",),
    "voiceml-php-sdk": ("src/Version.php",),
    "voiceml-swift": ("Sources/VoiceML/Version.swift",),
}


def api(repo, suffix):
    return json.loads(get(f"https://api.github.com/repos/voicetel/{repo}/{suffix}"))


def has_version(source, version):
    return bool(re.search(r'["\'>]' + re.escape(version) + r'["\'<]', source))


def check_candidate(repo, paths, version):
    sha = api(repo, "git/ref/heads/main")["object"]["sha"]
    errors = []
    for path in paths:
        content = api(repo, f"contents/{path}?ref={sha}")
        source = base64.b64decode(content["content"]).decode()
        if not has_version(source, version):
            errors.append(f"{path} does not declare {version}")

    workflows = ["ci.yml", "codeql.yml"]
    if repo == "voiceml-go-sdk":
        workflows.append("security-scan.yml")
    for workflow in workflows:
        runs = api(repo, f"actions/workflows/{workflow}/runs?event=push&branch=main&head_sha={sha}&per_page=1")
        items = runs["workflow_runs"]
        if not items or items[0]["head_sha"] != sha or items[0]["conclusion"] != "success":
            errors.append(f"{workflow} has no successful main push run for {sha}")

    existing = api(repo, f"git/matching-refs/tags/v{version}")
    if any(item["ref"] == f"refs/tags/v{version}" for item in existing):
        errors.append(f"tag v{version} already exists; do not move published tags")
    return sha, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", help="candidate SDK version without v")
    args = parser.parse_args()
    if not re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", args.version, re.ASCII):
        parser.error("version must be a stable major.minor.patch")
    failed = False
    for repo, paths in SDK_VERSIONS.items():
        sha, errors = check_candidate(repo, paths, args.version)
        print(f"{repo} {sha}: {'; '.join(errors) if errors else 'ready'}", flush=True)
        failed |= bool(errors)
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
