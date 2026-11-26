"""Tests for the static site builder: completeness, escaping and structured data."""

import json
import re
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import build_site  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ENTRIES = json.loads((ROOT / "data" / "entries.json").read_text())
VERIFICATION = {
    v["id"]: v for v in json.loads((ROOT / "data" / "verification.json").read_text())
}


def extract_json_ld(page: str) -> dict:
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', page, re.S)
    return json.loads(match.group(1))


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page, cls.sitemap = build_site.render(ENTRIES, VERIFICATION)
        cls.kept = [
            e for e in ENTRIES if VERIFICATION[e["id"]]["verdict"] in build_site.KEPT
        ]

    def test_every_entry_is_in_the_static_html(self):
        for e in self.kept:
            self.assertIn(f'href="{build_site.esc(e["url"])}"', self.page, e["name"])

    def test_json_ld_lists_every_entry(self):
        data = extract_json_ld(self.page)
        self.assertEqual(data["@type"], "CollectionPage")
        self.assertEqual(data["mainEntity"]["numberOfItems"], len(self.kept))
        self.assertEqual(len(data["mainEntity"]["itemListElement"]), len(self.kept))

    def test_head_has_seo_tags(self):
        for needle in (
            '<link rel="canonical"',
            'name="description"',
            'property="og:image"',
            'name="twitter:card"',
            "<title>Awesome Genealogy Dev",
        ):
            self.assertIn(needle, self.page)

    def test_description_is_search_snippet_sized(self):
        self.assertLessEqual(len(build_site.DESCRIPTION), 200)

    def test_sitemap_is_valid_xml_with_site_url(self):
        root = ET.fromstring(self.sitemap)
        locs = [
            el.text
            for el in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        ]
        self.assertEqual(locs, [build_site.SITE_URL])

    def test_hostile_text_is_escaped(self):
        evil = [
            dict(
                ENTRIES[0],
                name="<script>alert(1)</script>",
                desc="Bad </script><img src=x onerror=1>.",
            )
        ]
        page, _ = build_site.render(evil, {evil[0]["id"]: VERIFICATION[evil[0]["id"]]})
        self.assertNotIn("<script>alert(1)", page)
        self.assertNotIn("<img src=x", page)
        self.assertEqual(
            len(re.findall(r"</script>", page)), 2
        )  # JSON-LD and the filter script only

    def test_search_input_has_label(self):
        self.assertIn('<label for="q">', self.page)


if __name__ == "__main__":
    unittest.main()
