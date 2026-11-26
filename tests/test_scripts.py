"""Tests for the verification decision logic, data lint and README builder."""
import datetime as dt
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import build_readme  # noqa: E402
import lint_data  # noqa: E402
import verify  # noqa: E402

TODAY = dt.date(2026, 11, 26)
OK_HTTP = {"status": 200, "final_url": "https://x", "title": "X", "error": ""}


def repo(pushed="2026-10-01T00:00:00Z", archived=False):
    return {"full_name": "a/b", "archived": archived, "pushed_at": pushed, "license": "MIT", "stars": 1}


class DecideTests(unittest.TestCase):
    def test_active_repo_passes(self):
        self.assertEqual(verify.decide({"url": "u"}, OK_HTTP, repo(), {}, TODAY)[0], "pass")

    def test_archived_repo_fails(self):
        self.assertEqual(verify.decide({"url": "u"}, OK_HTTP, repo(archived=True), {}, TODAY)[0], "fail")

    def test_old_repo_fails_without_keep(self):
        self.assertEqual(verify.decide({"url": "u"}, OK_HTTP, repo("2023-01-01T00:00:00Z"), {}, TODAY)[0], "fail")

    def test_old_repo_with_keep_is_stale(self):
        self.assertEqual(
            verify.decide({"url": "u", "keep": True}, OK_HTTP, repo("2023-01-01T00:00:00Z"), {}, TODAY)[0], "stale")

    def test_very_old_repo_fails_even_with_keep(self):
        self.assertEqual(
            verify.decide({"url": "u", "keep": True}, OK_HTTP, repo("2019-01-01T00:00:00Z"), {}, TODAY)[0], "fail")

    def test_404_fails(self):
        http = dict(OK_HTTP, status=404)
        self.assertEqual(verify.decide({"url": "u"}, http, None, {}, TODAY)[0], "fail")

    def test_blocked_site_needs_manual_note(self):
        http = dict(OK_HTTP, status=403)
        self.assertEqual(verify.decide({"url": "u"}, http, None, {}, TODAY)[0], "fail")
        self.assertEqual(verify.decide({"url": "u"}, http, None, {"u": {"note": "n"}}, TODAY)[0], "manual")

    def test_bot_wall_with_http_200_is_not_a_pass(self):
        http = dict(OK_HTTP, title="Just a moment...")
        self.assertEqual(verify.decide({"url": "u"}, http, None, {}, TODAY)[0], "fail")
        self.assertEqual(verify.decide({"url": "u"}, http, None, {"u": {"note": "n"}}, TODAY)[0], "manual")

    def test_github_error_fails(self):
        self.assertEqual(verify.decide({"url": "u"}, OK_HTTP, {"error": "Not Found"}, {}, TODAY)[0], "fail")


class LintTests(unittest.TestCase):
    base = {"id": 0, "section": "Data Formats", "sub": "s", "name": "Thing", "url": "https://t.example", "desc": "A thing."}

    def run_lint(self, **changes):
        entry = dict(self.base, **changes)
        ver = [{"id": 0, "verdict": "pass", "reason": ""}]
        problems = lint_data.check([entry], ver, {})
        return [p for p in problems if "only 1 entries" not in p]

    def test_valid_entry_has_no_problems(self):
        self.assertEqual(self.run_lint(), [])

    def test_description_needs_period(self):
        self.assertTrue(any("period" in p for p in self.run_lint(desc="A thing")))

    def test_description_needs_capital(self):
        self.assertTrue(any("capital" in p for p in self.run_lint(desc="a thing.")))

    def test_description_must_not_repeat_name(self):
        self.assertTrue(any("repeats" in p for p in self.run_lint(desc="Thing does stuff.")))

    def test_unknown_section_is_rejected(self):
        self.assertTrue(any("unknown section" in p for p in self.run_lint(section="Nope")))

    def test_api_entry_requires_metadata(self):
        self.assertTrue(any("auth and limits" in p for p in self.run_lint(section="Record and Archive APIs")))

    def test_api_evidence_must_be_http(self):
        entry = dict(self.base, section="Record and Archive APIs",
                     api={"auth": "a", "limits": "b", "evidence": "javascript:alert(1)"})
        problems = lint_data.check([entry], [{"id": 0, "verdict": "pass", "reason": ""}], {})
        self.assertTrue(any("evidence must be http" in x for x in problems))

    def test_failed_verification_is_reported(self):
        problems = lint_data.check([dict(self.base)], [{"id": 0, "verdict": "fail", "reason": "HTTP 404"}], {})
        self.assertTrue(any("HTTP 404" in p for p in problems))

    def test_duplicate_url_is_reported(self):
        b = dict(self.base, id=1, name="Other")
        ver = [{"id": 0, "verdict": "pass", "reason": ""}, {"id": 1, "verdict": "pass", "reason": ""}]
        self.assertTrue(any("duplicate url" in p for p in lint_data.check([dict(self.base), b], ver, {})))


class RenderTests(unittest.TestCase):
    def test_anchor_matches_github_style(self):
        self.assertEqual(build_readme.anchor("Genealogy Apps (Open Source)"), "genealogy-apps-open-source")

    def test_stale_repo_line_says_low_activity(self):
        entry = {"name": "N", "url": "https://n.example", "desc": "D."}
        ver = {"verdict": "stale", "repo": repo("2023-01-01T00:00:00Z")}
        self.assertIn("low activity", build_readme.line_for(entry, ver))

    def test_api_line_has_auth_limits_and_source(self):
        entry = {"name": "N", "url": "https://n.example", "desc": "D.",
                 "api": {"auth": "None", "limits": "20 per minute", "evidence": "https://e.example"}}
        line = build_readme.line_for(entry, {"verdict": "pass", "repo": None})
        self.assertIn("**Auth:** None", line)
        self.assertIn("**Limits:** 20 per minute", line)
        self.assertIn("(https://e.example)", line)


class RealDataTests(unittest.TestCase):
    def test_committed_data_is_valid_and_readme_current(self):
        self.assertEqual(lint_data.main(), 0)
        self.assertEqual(build_readme.render(), (build_readme.ROOT / "README.md").read_text())


if __name__ == "__main__":
    unittest.main()
