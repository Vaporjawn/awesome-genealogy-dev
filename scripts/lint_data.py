#!/usr/bin/env python3
"""Validate data/entries.json against the rules in contributing.md.

Checks required fields, description style, duplicate names and URLs, API
metadata, and that every entry has a passing verification record.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REQUIRED = ("section", "sub", "name", "url", "desc")
SECTIONS = {
    "Data Formats", "Parsers and Converters", "Tree Visualization Libraries", "Genealogy Apps",
    "Record and Archive APIs", "DNA and Matching Tools", "OCR and Handwriting Recognition for Records",
    "Geocoding and Historical Places", "Data Models and Schemas", "Standards and Specs", "Research Guides",
}
OK_VERDICTS = {"pass", "stale", "manual"}


def check(entries: list[dict], verification: list[dict], manual: dict) -> list[str]:
    """Return a list of human-readable problems; empty means the data is valid."""
    problems: list[str] = []
    ver = {v["id"]: v for v in verification}
    seen_names: dict[tuple[str, str], int] = {}
    seen_urls: dict[str, int] = {}
    seen_ids: set[int] = set()
    for e in entries:
        label = f"#{e.get('id')} {e.get('name')}"
        for key in REQUIRED:
            if not e.get(key):
                problems.append(f"{label}: missing {key}")
        if e.get("id") in seen_ids:
            problems.append(f"{label}: duplicate id")
        seen_ids.add(e.get("id"))
        if e.get("section") not in SECTIONS:
            problems.append(f"{label}: unknown section {e.get('section')!r}")
        desc = e.get("desc", "")
        if desc and not re.match(r"^[A-Z0-9(.]", desc):
            problems.append(f"{label}: description must start with a capital letter")
        if desc and not desc.endswith("."):
            problems.append(f"{label}: description must end with a period")
        if desc and desc.lower().startswith(e.get("name", "").lower() + " "):
            problems.append(f"{label}: description repeats the name")
        if not str(e.get("url", "")).startswith(("https://", "http://")):
            problems.append(f"{label}: url must be http(s)")
        name_key = (e.get("section", ""), e.get("name", "").lower())
        if name_key in seen_names:
            problems.append(f"{label}: duplicate name within section (also #{seen_names[name_key]})")
        seen_names[name_key] = e.get("id")
        url_key = e.get("url", "").lower().rstrip("/")
        if url_key in seen_urls:
            problems.append(f"{label}: duplicate url (also #{seen_urls[url_key]})")
        seen_urls[url_key] = e.get("id")
        api = e.get("api")
        if api:
            for key in ("auth", "limits", "evidence"):
                if not api.get(key):
                    problems.append(f"{label}: api.{key} missing")
        if e["section"] == "Record and Archive APIs" and not api and not e.get("repo"):
            problems.append(f"{label}: API entry without auth and limits metadata")
        v = ver.get(e["id"])
        if v is None:
            problems.append(f"{label}: no verification record; run scripts/verify.py")
        elif v["verdict"] not in OK_VERDICTS:
            problems.append(f"{label}: verification verdict {v['verdict']}: {v['reason']}")
        elif v["verdict"] == "manual" and e["url"] not in manual:
            problems.append(f"{label}: manual verdict without entry in data/manual-checks.json")
    if len(entries) < 50:
        problems.append(f"only {len(entries)} entries; the target is 50+")
    return problems


def main() -> int:
    entries = json.loads((DATA / "entries.json").read_text())
    verification = json.loads((DATA / "verification.json").read_text())
    manual = json.loads((DATA / "manual-checks.json").read_text())
    problems = check(entries, verification, manual)
    for p in problems:
        print("data lint:", p)
    if problems:
        return 1
    print(f"data lint: {len(entries)} entries ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
