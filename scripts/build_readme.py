#!/usr/bin/env python3
"""Generate README.md from data/entries.json and data/verification.json.

The README is a build artifact: edit data/entries.json (or data/header.md and
data/footer.md), run this script, and commit the result. ``--check`` exits
non-zero when README.md is out of date, which CI uses.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

SECTION_ORDER = [
    ("Data Formats", "Data Formats"),
    ("Parsers and Converters", "Parsers and Converters"),
    ("Tree Visualization Libraries", "Tree Visualization Libraries"),
    ("Genealogy Apps", "Genealogy Apps (Open Source)"),
    ("Record and Archive APIs", "Record and Archive APIs"),
    ("DNA and Matching Tools", "DNA and Matching Tools"),
    ("OCR and Handwriting Recognition for Records", "OCR and Handwriting Recognition for Records"),
    ("Geocoding and Historical Places", "Geocoding and Historical Places"),
    ("Data Models and Schemas", "Data Models and Schemas"),
    ("Standards and Specs", "Standards and Specs"),
    ("Research Guides", "Research Guides"),
]


def anchor(title: str) -> str:
    """GitHub-style heading anchor."""
    slug = re.sub(r"[^\w\- ]", "", title.lower()).strip().replace(" ", "-")
    return slug


def line_for(entry: dict, ver: dict) -> str:
    """Render one README list item."""
    parts = [f"- [{entry['name']}]({entry['url']}) - {entry['desc']}"]
    api = entry.get("api")
    if api:
        parts.append(f" **Auth:** {api['auth']}. **Limits:** {api['limits']}. ([source]({api['evidence']}))")
    facts = []
    repo = ver.get("repo")
    if repo and not repo.get("error"):
        facts.append(repo["license"] or "no license")
        suffix = f"last push {repo['pushed_at'][:7]}"
        if ver["verdict"] == "stale":
            suffix += ", low activity"
        facts.append(suffix)
    elif ver["verdict"] == "manual":
        facts.append("checked by hand, bot-blocked")
    if facts:
        parts.append(f" *{', '.join(facts)}.*")
    return "".join(parts)


def render() -> str:
    entries = json.loads((DATA / "entries.json").read_text())
    verification = {v["id"]: v for v in json.loads((DATA / "verification.json").read_text())}
    checked = max(v["checked"] for v in verification.values())
    kept = [e for e in entries if verification.get(e["id"], {}).get("verdict") in ("pass", "stale", "manual")]

    by_section: dict[str, dict[str, list[str]]] = {}
    for e in kept:
        by_section.setdefault(e["section"], {}).setdefault(e["sub"], []).append(line_for(e, verification[e["id"]]))

    header = (DATA / "header.md").read_text().replace("{{COUNT}}", str(len(kept))).replace("{{CHECKED}}", checked)
    footer = (DATA / "footer.md").read_text()

    toc = ["## Contents", ""]
    toc += [f"- [{title}](#{anchor(title)})" for key, title in SECTION_ORDER if key in by_section]
    toc += [""]

    body: list[str] = []
    for key, title in SECTION_ORDER:
        if key not in by_section:
            continue
        body += [f"## {title}", ""]
        for sub, lines in by_section[key].items():
            body += [f"### {sub}", ""] + lines + [""]
    unknown = set(by_section) - {k for k, _ in SECTION_ORDER}
    if unknown:
        raise SystemExit(f"entries use unknown sections: {sorted(unknown)}")
    return header.rstrip() + "\n\n" + "\n".join(toc) + "\n" + "\n".join(body).rstrip() + "\n\n" + footer.lstrip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if README.md is out of date")
    args = parser.parse_args()
    text = render()
    target = ROOT / "README.md"
    if args.check:
        if not target.exists() or target.read_text() != text:
            print("README.md is out of date; run python3 scripts/build_readme.py", file=sys.stderr)
            return 1
        print("README.md is up to date")
        return 0
    target.write_text(text)
    print(f"wrote README.md ({text.count(chr(10))} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
