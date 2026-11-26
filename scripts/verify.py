#!/usr/bin/env python3
"""Verify every entry in data/entries.json against the live web.

For each entry it records:
  * the HTTP status of the entry URL (after redirects);
  * for GitHub-backed entries, repository metadata from the GitHub API
    (archived flag, last push, SPDX license, stars, canonical name);
  * a verdict: ``pass``, ``stale`` (kept only when flagged ``keep``), ``fail`` or
    ``manual`` (site blocks bots; needs an override in data/manual-checks.json).

Output is written to data/verification.json. Standard library only; GitHub data
comes from the ``gh`` CLI when present, otherwise from GITHUB_TOKEN.

Usage:
    python3 scripts/verify.py                # verify everything
    python3 scripts/verify.py --only 12 40   # verify specific entry ids
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
USER_AGENT = "Mozilla/5.0 (compatible; awesome-genealogy-dev-verifier/1.0; +https://github.com/Vaporjawn/awesome-genealogy-dev)"
ACTIVE_MONTHS = 24  # repos pushed within this window count as active
MAX_STALE_MONTHS = 60  # even with keep=true, anything older fails
BOT_BLOCKED = {401, 403, 405, 429, 503, 999}
BOT_WALL = re.compile(r"just a moment|not a bot|pardon our interruption|access denied|attention required|one moment, please|temporarily unavailable", re.I)


def months_since(iso: str, today: dt.date) -> int:
    pushed = dt.date.fromisoformat(iso[:10])
    return (today.year - pushed.year) * 12 + (today.month - pushed.month)


def http_check(url: str) -> dict:
    """Fetch the first 100 KB of a URL with curl and report status, final URL and page title.

    curl is used instead of urllib so the system certificate store applies.
    """
    marker = "\n##CURLMETA##"
    try:
        out = subprocess.run(
            ["curl", "-sSL", "-m", "30", "--retry", "2", "-A", USER_AGENT, "-r", "0-100000",
             "-w", f"{marker}%{{http_code}}|%{{url_effective}}", url],
            capture_output=True, timeout=120,
        )
    except Exception as err:  # noqa: BLE001 - failures are data here
        return {"status": 0, "final_url": url, "title": "", "error": f"{type(err).__name__}: {err}"}
    body, _, tail = out.stdout.decode("utf-8", "replace").rpartition(marker)
    code, _, final = tail.partition("|")
    status = int(code) if code.isdigit() else 0
    match = re.search(r"(?is)<title[^>]*>(.*?)</title>", body)
    title = re.sub(r"\s+", " ", html.unescape(match.group(1))).strip()[:120] if match else ""
    error = out.stderr.decode("utf-8", "replace").strip()[:160] if status == 0 else ""
    if status == 416:  # server rejected the range request; the page exists
        status = 200
    return {"status": status, "final_url": final or url, "title": title, "error": error}


def github_repo(slug: str) -> dict | None:
    """Fetch repository metadata through gh or the REST API."""
    try:
        if shutil.which("gh"):
            out = subprocess.run(
                ["gh", "api", f"repos/{slug}"],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if out.returncode != 0:
                return {"error": out.stderr.strip()[:200] or "gh api failed"}
            raw = json.loads(out.stdout)
        else:
            headers = {
                "User-Agent": USER_AGENT,
                "Accept": "application/vnd.github+json",
            }
            if os.environ.get("GITHUB_TOKEN"):
                headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
            request = urllib.request.Request(
                f"https://api.github.com/repos/{slug}", headers=headers
            )
            with urllib.request.urlopen(request, timeout=30) as response:
                raw = json.load(response)
    except Exception as err:  # noqa: BLE001
        return {"error": f"{type(err).__name__}: {err}"[:200]}
    license_info = raw.get("license") or {}
    return {
        "full_name": raw.get("full_name"),
        "archived": bool(raw.get("archived")),
        "pushed_at": raw.get("pushed_at"),
        "license": license_info.get("spdx_id")
        if license_info.get("spdx_id") not in (None, "NOASSERTION")
        else None,
        "stars": raw.get("stargazers_count"),
        "description": raw.get("description"),
        "language": raw.get("language"),
    }


def decide(
    entry: dict, http: dict, repo: dict | None, manual: dict, today: dt.date
) -> tuple[str, str]:
    """Return (verdict, reason)."""
    if repo is not None:
        if repo.get("error"):
            return "fail", f"GitHub API: {repo['error']}"
        if repo["archived"]:
            return "fail", "repository is archived"
        age = months_since(repo["pushed_at"], today)
        if age > MAX_STALE_MONTHS:
            return "fail", f"last push {age} months ago"
        if age > ACTIVE_MONTHS and not entry.get("keep"):
            return "fail", f"last push {age} months ago and not marked keep"
        if age > ACTIVE_MONTHS:
            return "stale", f"last push {age} months ago; kept as stable reference"
    status = http["status"]
    if status and status < 400 and not BOT_WALL.search(http.get("title", "")):
        return "pass", ""
    key = entry["url"]
    if key in manual:
        return "manual", manual[key]["note"]
    if status in BOT_BLOCKED or BOT_WALL.search(http.get("title", "")):
        return (
            "fail",
            f"HTTP {status} (bot-blocked): add a note to data/manual-checks.json after checking by hand",
        )
    return "fail", f"HTTP {status or 'no response'} {http['error']}".strip()


def verify_one(entry: dict, manual: dict, today: dt.date) -> dict:
    http = http_check(entry["url"])
    repo = github_repo(entry["repo"]) if entry.get("repo") else None
    verdict, reason = decide(entry, http, repo, manual, today)
    return {
        "id": entry["id"],
        "name": entry["name"],
        "url": entry["url"],
        "http": http,
        "repo": repo,
        "verdict": verdict,
        "reason": reason,
        "checked": today.isoformat(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--only", nargs="*", type=int, help="verify only these entry ids"
    )
    parser.add_argument("--today", help="override today's date (YYYY-MM-DD), for tests")
    args = parser.parse_args()

    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    entries = json.loads((DATA / "entries.json").read_text())
    manual_path = DATA / "manual-checks.json"
    manual = json.loads(manual_path.read_text()) if manual_path.exists() else {}
    out_path = DATA / "verification.json"
    previous = (
        {r["id"]: r for r in json.loads(out_path.read_text())}
        if out_path.exists() and args.only
        else {}
    )

    todo = [e for e in entries if not args.only or e["id"] in args.only]
    with ThreadPoolExecutor(max_workers=10) as pool:
        results = list(pool.map(lambda e: verify_one(e, manual, today), todo))
    for r in results:
        previous[r["id"]] = r
    merged = [previous[k] for k in sorted(previous)]
    out_path.write_text(json.dumps(merged, indent=1, ensure_ascii=False) + "\n")

    counts: dict[str, int] = {}
    for r in merged:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    print("verdicts:", counts)
    for r in merged:
        if r["verdict"] in ("fail", "manual", "stale"):
            print(f"  [{r['verdict']}] {r['id']:>3} {r['name']}: {r['reason']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
