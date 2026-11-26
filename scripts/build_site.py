#!/usr/bin/env python3
"""Build the static, searchable GitHub Pages site from data/entries.json.

Output goes to ``site/`` (git-ignored; the Pages workflow builds and deploys it):

* ``index.html``  every entry rendered as plain HTML (so search engines index
  it without running JavaScript) plus a small client-side filter;
* ``sitemap.xml`` and ``robots.txt``;
* ``social.png``  copied from ``assets/`` when present, for link previews.

The page carries a title, meta description, canonical URL, Open Graph and
Twitter tags, and JSON-LD (``CollectionPage`` with an ``ItemList``).
"""

from __future__ import annotations

import html
import json
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "site"
SITE_URL = "https://vaporjawn.dev/awesome-genealogy-dev/"
REPO_URL = "https://github.com/Vaporjawn/awesome-genealogy-dev"
TITLE = (
    "Awesome Genealogy Dev: GEDCOM parsers, family tree libraries and genealogy APIs"
)
DESCRIPTION = (
    "Searchable, verified list of GEDCOM parsers, family tree chart libraries, genealogy APIs, DNA and "
    "record-linkage tools, handwriting OCR, historical gazetteers, schemas and standards for developers."
)
SECTION_TITLES = {"Genealogy Apps": "Genealogy Apps (Open Source)"}
KEPT = ("pass", "stale", "manual")

CSS = """
:root{--bg:#fbfaf7;--fg:#1d2330;--muted:#5a6275;--line:#dcd8cf;--card:#fff;--accent:#1f5f8b;--chip:#eef3f7;--mark:#ffe58a}
@media (prefers-color-scheme:dark){:root{--bg:#14171e;--fg:#e8eaf0;--muted:#a3abbd;--line:#2c3340;--card:#1b1f28;--accent:#7cc0ee;--chip:#222a36;--mark:#6b5a12}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--accent)}
.wrap{max-width:60rem;margin:0 auto;padding:0 16px}
header.top{padding:40px 0 20px;border-bottom:1px solid var(--line)}
h1{font-size:clamp(1.7rem,4vw,2.4rem);line-height:1.15;margin:0 0 .5rem}
.lede{color:var(--muted);margin:0 0 1rem;max-width:44rem}
.meta{color:var(--muted);font-size:.9rem}
.search{position:sticky;top:0;z-index:2;background:var(--bg);padding:12px 0;border-bottom:1px solid var(--line)}
.search label{display:block;font-weight:600;margin-bottom:6px}
.search input{width:100%;padding:10px 12px;font:inherit;color:var(--fg);background:var(--card);border:1px solid var(--line);border-radius:8px}
.search input:focus-visible,a:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px;padding:0;list-style:none}
.chips a{display:inline-block;padding:4px 10px;border-radius:999px;background:var(--chip);text-decoration:none;font-size:.85rem;color:var(--fg)}
.status{color:var(--muted);font-size:.9rem;margin:10px 0 0}
section{padding-top:28px}
h2{font-size:1.4rem;margin:0 0 .25rem}
h3{font-size:1rem;margin:1.2rem 0 .4rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
ul.entries{list-style:none;margin:0;padding:0}
ul.entries li{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin:0 0 8px}
ul.entries li a.name{font-weight:650}
.desc{margin:.2rem 0 0}
.facts{margin:.35rem 0 0;color:var(--muted);font-size:.85rem}
.facts strong{color:var(--fg)}
mark{background:var(--mark);color:inherit;border-radius:3px}
footer{margin:48px 0;color:var(--muted);font-size:.9rem;border-top:1px solid var(--line);padding-top:16px}
.hidden{display:none}
"""

JS = """
(function(){
  var input=document.getElementById('q'),status=document.getElementById('status');
  var items=[].slice.call(document.querySelectorAll('ul.entries li'));
  var groups=[].slice.call(document.querySelectorAll('section[data-section]'));
  var text=items.map(function(li){return li.textContent.toLowerCase();});
  function run(){
    var terms=input.value.toLowerCase().split(/\\s+/).filter(Boolean),shown=0;
    items.forEach(function(li,i){
      var ok=terms.every(function(t){return text[i].indexOf(t)!==-1;});
      li.classList.toggle('hidden',!ok); if(ok)shown++;
    });
    groups.forEach(function(g){
      g.classList.toggle('hidden',!g.querySelector('ul.entries li:not(.hidden)'));
    });
    status.textContent=terms.length?(shown+' of '+items.length+' entries match'):(items.length+' entries');
  }
  input.addEventListener('input',run);
  document.addEventListener('keydown',function(e){
    if(e.key==='/'&&document.activeElement!==input){e.preventDefault();input.focus();}
  });
  var initial=new URLSearchParams(location.search).get('q');
  if(initial){input.value=initial;}
  run();
})();
"""


def safe_url(url: str) -> str:
    """Return the URL unchanged when it is http(s); raise otherwise.

    The URLs come from data/entries.json and end up in href attributes, so a
    ``javascript:`` or ``data:`` URL must stop the build instead of shipping.
    """
    if urlparse(url).scheme not in ("http", "https"):
        raise ValueError(f"refusing non-http(s) URL: {url!r}")
    return url


def esc(value: str) -> str:
    """HTML-escape text for element content and attribute values."""
    return html.escape(value, quote=True)


def entry_facts(entry: dict, ver: dict) -> str:
    """Render the small facts line under an entry (license, activity, auth, limits)."""
    facts = []
    api = entry.get("api")
    if api:
        facts.append(f"<strong>Auth:</strong> {esc(api['auth'])}")
        facts.append(f"<strong>Limits:</strong> {esc(api['limits'])}")
        facts.append(f'<a href="{esc(safe_url(api["evidence"]))}" rel="noopener">source</a>')
    repo = ver.get("repo")
    if repo and not repo.get("error"):
        facts.append(esc(repo["license"] or "no license"))
        activity = f"last push {repo['pushed_at'][:7]}"
        facts.append(
            esc(activity + (", low activity" if ver["verdict"] == "stale" else ""))
        )
    elif ver["verdict"] == "manual":
        facts.append("checked by hand, bot-blocked")
    return f'<p class="facts">{" · ".join(facts)}</p>' if facts else ""


def render(entries: list[dict], verification: dict[int, dict]) -> tuple[str, str]:
    """Return (index.html, sitemap.xml) for the kept entries."""
    kept = [e for e in entries if verification.get(e["id"], {}).get("verdict") in KEPT]
    checked = max(v["checked"] for v in verification.values())

    sections: dict[str, dict[str, list[dict]]] = {}
    for e in kept:
        sections.setdefault(e["section"], {}).setdefault(e["sub"], []).append(e)

    chips, body = [], []
    for name, subs in sections.items():
        title = SECTION_TITLES.get(name, name)
        anchor = "".join(c if c.isalnum() else "-" for c in title.lower()).strip("-")
        anchor = "-".join(part for part in anchor.split("-") if part)
        chips.append(f'<li><a href="#{anchor}">{esc(title)}</a></li>')
        body.append(f'<section id="{anchor}" data-section><h2>{esc(title)}</h2>')
        for sub, items in subs.items():
            body.append(f'<h3>{esc(sub)}</h3><ul class="entries">')
            for e in items:
                body.append(
                    f'<li><a class="name" href="{esc(safe_url(e["url"]))}" rel="noopener">{esc(e["name"])}</a>'
                    f'<p class="desc">{esc(e["desc"])}</p>{entry_facts(e, verification[e["id"]])}</li>'
                )
            body.append("</ul>")
        body.append("</section>")

    json_ld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": TITLE,
        "description": DESCRIPTION,
        "url": SITE_URL,
        "inLanguage": "en",
        "dateModified": checked,
        "license": "https://creativecommons.org/publicdomain/zero/1.0/",
        "author": {
            "@type": "Person",
            "name": "Victor Williams",
            "url": "https://github.com/Vaporjawn",
        },
        "isBasedOn": REPO_URL,
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(kept),
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": i + 1,
                    "name": e["name"],
                    "url": e["url"],
                    "description": e["desc"],
                }
                for i, e in enumerate(kept)
            ],
        },
    }
    ld = json.dumps(json_ld, ensure_ascii=False).replace("<", "\\u003c")
    social = SITE_URL + "social.png"

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(TITLE)}</title>
<meta name="description" content="{esc(DESCRIPTION)}">
<link rel="canonical" href="{SITE_URL}">
<meta name="keywords" content="genealogy, GEDCOM, family tree, GEDCOM parser, GEDCOM X, FamilySearch API, WikiTree API, genealogy API, genealogy software, handwriting recognition, historical gazetteer, record linkage">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(TITLE)}">
<meta property="og:description" content="{esc(DESCRIPTION)}">
<meta property="og:url" content="{SITE_URL}">
<meta property="og:image" content="{social}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(TITLE)}">
<meta name="twitter:description" content="{esc(DESCRIPTION)}">
<meta name="twitter:image" content="{social}">
<style>{CSS}</style>
<script type="application/ld+json">{ld}</script>
</head>
<body>
<header class="top"><div class="wrap">
<h1>Awesome Genealogy Dev</h1>
<p class="lede">Verified libraries, formats, APIs and tools for developers building genealogy and family-tree software: GEDCOM parsers, tree visualization, record and archive APIs, DNA and record linkage, handwriting recognition, historical places, schemas and standards.</p>
<p class="meta">{len(kept)} entries, each checked on {esc(checked)}. Source and contributions on <a href="{REPO_URL}">GitHub</a>. How entries are verified: <a href="{REPO_URL}/blob/main/docs/METHODOLOGY.md">methodology</a>.</p>
</div></header>
<div class="search"><div class="wrap">
<label for="q">Search entries (press / to focus)</label>
<input id="q" type="search" placeholder="Try gedcom, python, oauth, ocr, gazetteer" autocomplete="off">
<p class="status" id="status" aria-live="polite">{len(kept)} entries</p>
<nav aria-label="Sections"><ul class="chips">{"".join(chips)}</ul></nav>
</div></div>
<main class="wrap">
{"".join(body)}
</main>
<footer><div class="wrap">Released under <a href="https://creativecommons.org/publicdomain/zero/1.0/">CC0 1.0</a> by <a href="https://github.com/Vaporjawn">Victor Williams</a>. <a href="{REPO_URL}">View the repository</a>.</div></footer>
<script>{JS}</script>
</body>
</html>
"""
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url><loc>{SITE_URL}</loc><lastmod>{checked}</lastmod><changefreq>weekly</changefreq></url>\n"
        "</urlset>\n"
    )
    return page, sitemap


def main() -> int:
    entries = json.loads((DATA / "entries.json").read_text())
    verification = {
        v["id"]: v for v in json.loads((DATA / "verification.json").read_text())
    }
    page, sitemap = render(entries, verification)
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    (OUT / "index.html").write_text(page)
    (OUT / "sitemap.xml").write_text(sitemap)
    (OUT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n"
    )
    (OUT / ".nojekyll").write_text("")
    social = ROOT / "assets" / "social.png"
    if social.exists():
        shutil.copy(social, OUT / "social.png")
    print(f"wrote site/ ({len(page)} bytes of HTML)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
