import base64
import unittest
from unittest.mock import patch

import check_release_candidates as release
import dependabot_queue as queue


class CandidateTests(unittest.TestCase):
    def test_source_versions_are_exact(self):
        self.assertTrue(release.has_version('<version>0.9.6</version>', '0.9.6'))
        self.assertTrue(release.has_version('version = "0.9.6"', '0.9.6'))
        self.assertFalse(release.has_version('version = "0.9.60"', '0.9.6'))

    def test_reused_tag_and_stale_checks_are_not_ready(self):
        def api(repo, suffix):
            if suffix.startswith("git/ref/heads/"):
                return {"object": {"sha": "new"}}
            if suffix.startswith("contents/"):
                return {"content": base64.b64encode(b'version = "0.9.6"')}
            if suffix.startswith("actions/"):
                return {"workflow_runs": [{"head_sha": "old", "conclusion": "success"}]}
            return [{"ref": "refs/tags/v0.9.6"}]

        with patch.object(release, "api", side_effect=api):
            sha, errors = release.check_candidate("voiceml-python-sdk", ("version.py",), "0.9.6")
        self.assertEqual(sha, "new")
        self.assertEqual(len(errors), 3)


class QueueTests(unittest.TestCase):
    def setUp(self):
        self.repo = "voicetel/voiceml-node-sdk"
        self.pr = {"draft": False, "user": {"login": "dependabot[bot]"}, "number": 7,
                   "head": {"sha": "head", "repo": {"full_name": self.repo}},
                   "base": {"ref": "main"}, "title": "Bump a dependency"}
        self.state = {"headRefOid": "head", "mergeStateStatus": "CLEAN", "mergeable": "MERGEABLE",
                      "reviewDecision": "", "files": [{"path": "package-lock.json"}],
                      "statusCheckRollup": [{"conclusion": "SUCCESS"}]}
        self.comparison = {"behind_by": 0, "total_commits": 1,
                           "commits": [{"commit": {"message": "Bump a dependency"}}]}
        self.runs = {"workflow_runs": [{"head_sha": "head", "conclusion": "success",
                                       "pull_requests": [{"number": 7}]}]}

    def evaluate(self):
        with patch.object(queue, "gh", side_effect=[self.state, self.comparison, self.runs, self.runs]):
            return queue.gate(self.repo, self.pr)

    def test_eligible_exact_head(self):
        self.assertEqual(self.evaluate(), (7, "head", "Bump a dependency (#7)"))

    def test_workflow_changes_are_not_eligible(self):
        self.state["files"].append({"path": ".github/workflows/ci.yml"})
        self.assertIsNone(self.evaluate())

    def test_failed_check_or_stale_branch_is_not_eligible(self):
        self.comparison["behind_by"] = 1
        self.assertIsNone(self.evaluate())
        self.comparison["behind_by"] = 0
        self.state["statusCheckRollup"].append({"conclusion": "FAILURE"})
        self.assertIsNone(self.evaluate())

    def test_results_from_other_head_are_not_eligible(self):
        self.runs["workflow_runs"][0]["head_sha"] = "old"
        self.assertIsNone(self.evaluate())


if __name__ == "__main__":
    unittest.main()
