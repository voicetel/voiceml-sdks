"""Compile catalogue quickstarts without executing API requests."""

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]


def blocks(language: str) -> list[str]:
    return re.findall(rf"^```{language}\n(.*?)^```", (ROOT / "README.md").read_text(), re.M | re.S)


def run(command: list[str], cwd: Path, env: dict[str, str]) -> None:
    subprocess.run(command, cwd=cwd, env=env, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--go-module", type=Path, help="Read-only local Go SDK replacement")
    parser.add_argument("--typescript-package", type=Path, help="Local built npm tarball or package")
    args = parser.parse_args()
    # Compile against the latest SDK release in the README's release table, which can be
    # ahead of the API spec version shown on the badge.
    tags = re.findall(r"https://github.com/voicetel/[^/]+/releases/tag/v([\d.]+)", (ROOT / "README.md").read_text())
    version = max(tags, key=lambda v: tuple(int(x) for x in v.split(".")))
    env = os.environ.copy()
    env["GOWORK"] = "off"
    args.scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="examples-", dir=args.scratch) as temporary:
        scratch = Path(temporary)
        go = scratch / "go"
        go.mkdir()
        go_blocks = blocks("go")
        if len(go_blocks) != 1:
            raise ValueError("Expected one complete Go quickstart")
        (go / "main.go").write_text(go_blocks[0])
        module = f"module catalogue-example\n\ngo 1.21\n\nrequire github.com/voicetel/voiceml-go-sdk v{version}\n"
        if args.go_module:
            module += f"\nreplace github.com/voicetel/voiceml-go-sdk => {json.dumps(str(args.go_module.resolve()))}\n"
        (go / "go.mod").write_text(module)
        run(["go", "mod", "tidy"], go, env)
        run(["go", "vet", "./..."], go, env)
        run(["go", "build", "-o", str(go / "example"), "./..."], go, env)
        print("Go quickstart: build and vet passed", flush=True)

        ts = scratch / "typescript"
        ts.mkdir()
        (ts / "package.json").write_text(json.dumps({"private": True, "type": "module"}))
        package = str(args.typescript_package.resolve()) if args.typescript_package else f"@voicetel.com/voiceml@{version}"
        run(["npm", "install", "--ignore-scripts", "--no-package-lock", "typescript@6", package], ts, env)
        ts_blocks = blocks("ts")
        if len(ts_blocks) != 1:
            raise ValueError("Expected one TypeScript quickstart")
        (ts / "example.mts").write_text(ts_blocks[0])
        run([
            str(ts / "node_modules/.bin/tsc"), "--strict", "--noEmit",
            "--target", "ES2022", "--module", "NodeNext", "--moduleResolution", "NodeNext", "example.mts",
        ], ts, env)
        print("TypeScript quickstart: strict typecheck passed", flush=True)


if __name__ == "__main__":
    main()
