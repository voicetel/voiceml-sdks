"""Evaluate Dependabot lockfile updates without checking out PR code."""

import argparse
import json
import re
import subprocess

from check_release_candidates import SDK_VERSIONS


LOCKFILES = {"Gemfile.lock", "composer.lock", "package-lock.json"}
ATTRIBUTION = re.compile(
    r"co-authored-by:\s*(claude|cursor|copilot|chatgpt|gpt|anthropic|openai)"
    r"|generated with (claude|cursor|copilot|chatgpt|gpt|ai)|🤖|cursoragent"
    r"|written by (claude|cursor|copilot|chatgpt|gpt)",
    re.IGNORECASE,
)


def gh(*args):
    result = subprocess.run(["gh", *args], check=True, capture_output=True, text=True, timeout=35)
    return json.loads(result.stdout)


def gate(repo, pr):
    if pr["user"]["login"] != "dependabot[bot]" or pr["draft"]:
        return None
    if pr["head"]["repo"]["full_name"] != repo or pr["base"]["ref"] != "main":
        return None
    number, head = pr["number"], pr["head"]["sha"]
    state = gh("pr", "view", str(number), "-R", repo, "--json",
               "headRefOid,mergeStateStatus,mergeable,reviewDecision,statusCheckRollup,files")
    if (state["headRefOid"] != head or state["mergeStateStatus"] != "CLEAN"
            or state["mergeable"] != "MERGEABLE"
            or state["reviewDecision"] in ("CHANGES_REQUESTED", "REVIEW_REQUIRED")):
        return None
    files = {file["path"] for file in state["files"]}
    if not files or not files <= LOCKFILES:
        return None
    comparison = gh("api", f"repos/{repo}/compare/main...{head}")
    commits = comparison["commits"]
    # Require the exact current base, not merely a speculative merge.
    if comparison["behind_by"] or not commits or len(commits) != comparison["total_commits"]:
        return None
    if any(ATTRIBUTION.search(c["commit"]["message"]) for c in commits):
        return None
    conclusions = [c.get("conclusion") or c.get("state") or c.get("status")
                   for c in state["statusCheckRollup"]]
    if not conclusions or any(c not in {"SUCCESS", "SKIPPED", "NEUTRAL"} for c in conclusions):
        return None
    for workflow in ("ci.yml", "codeql.yml"):
        runs = gh("api", f"repos/{repo}/actions/workflows/{workflow}/runs?event=pull_request&head_sha={head}&per_page=20")
        if not any(r["head_sha"] == head and r["conclusion"] == "success"
                   and any(p["number"] == number for p in r["pull_requests"])
                   for r in runs["workflow_runs"]):
            return None
    title = f'{pr["title"]} (#{number})'
    if ATTRIBUTION.search(title):
        return None
    return number, head, title


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--merge", action="store_true", help="squash eligible PRs; default is report-only")
    args = parser.parse_args()
    for name in SDK_VERSIONS:
        repo = f"voicetel/{name}"
        if args.merge:
            rules = gh("api", f"repos/{repo}/rules/branches/main")
            if not any(rule["type"] == "required_status_checks"
                       and rule["parameters"].get("strict_required_status_checks_policy")
                       and rule["parameters"].get("required_status_checks")
                       for rule in rules):
                print(f"{repo}: report-only until main has strict required checks", flush=True)
                continue
        # Process at most one PR per repo per run. GitHub still enforces
        # its review and protection rules; do not use admin merge.
        for pr in gh("api", f"repos/{repo}/pulls?state=open&base=main&per_page=100&sort=created&direction=asc"):
            candidate = gate(repo, pr)
            if not candidate:
                continue
            number, head, title = candidate
            print(f"{repo}#{number} {head}: eligible", flush=True)
            if args.merge:
                result = gh("api", "-X", "PUT", f"repos/{repo}/pulls/{number}/merge",
                            "-f", "merge_method=squash", "-f", f"sha={head}",
                            "-f", f"commit_title={title}", "-f", f"commit_message=Dependabot pull request #{number}.")
                if not result["merged"]:
                    raise RuntimeError(f"{repo}#{number} did not merge")
                print(f"{repo}#{number}: merged {result['sha']}", flush=True)
            break
        else:
            print(f"{repo}: no eligible update", flush=True)


if __name__ == "__main__":
    main()
