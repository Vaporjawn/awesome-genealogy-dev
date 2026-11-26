# Awesome Genealogy Dev [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> Libraries, formats, APIs and tools for developers building genealogy and family-tree software.

This list is for people who write genealogy software, not for people researching their own tree. It covers file formats and specs, parsers, chart libraries, open-source apps, record-archive APIs, DNA and record-linkage tooling, handwriting recognition, historical geocoding, schemas and standards.

Looking for a GEDCOM parser, a GEDCOM 7 or GEDCOM X library, a family tree chart library for JavaScript or Python, a genealogy API (FamilySearch, WikiTree, Geni, national archives), a DNA segment or kinship tool, handwriting recognition for historical records, or a historical gazetteer? Each is a section below, and each API entry states its auth and rate limits.

Every one of the {{COUNT}} entries was checked against the live web on {{CHECKED}}: the URL answers, GitHub repositories are not archived, and descriptions restate what the project or page says about itself. [How entries are verified](docs/METHODOLOGY.md) and how this list differs from the older GEDCOM and genealogy lists are written down.

How to read an entry:

- *Italic notes* after a repository give its license and the month of its last push. "Low activity" means no push for more than 24 months; those entries stay only as stable references.
- **Auth** and **Limits** on API entries come from the provider's own documentation, linked as "source". When a limit could not be found, the entry says "not verified" or "not published" instead of guessing.
- "Checked by hand, bot-blocked" means the site refuses automated requests, so the entry was confirmed another way; the evidence is in [data/manual-checks.json](data/manual-checks.json).
- There is no single standard called "GENEALOGY JSON". The Data Formats section lists the real JSON options and says how mature each one is.
