# Methodology

How entries get into this list, how they are verified, and how the list compares with the older ones. Figures are from 2026-11-26.

## What a verified entry means

`python3 scripts/verify.py` checks every entry in `data/entries.json` and writes `data/verification.json`:

| Check | Source | Fails when |
| --- | --- | --- |
| URL answers | `curl`, first 100 KB, redirects followed | HTTP error, no response, or a bot-challenge page |
| Repository status | GitHub API (`gh api repos/<owner>/<name>`) | repository archived, renamed away, or missing |
| Freshness | `pushed_at` from the same call | no push for more than 24 months and not marked `keep`, or more than 60 months even with `keep` |
| License | SPDX id from the same call | never fails; "no license" is shown on the line |

Verdicts: `pass`, `stale` (kept as a stable reference, shown as "low activity"), `manual` (bot-blocked site confirmed another way, with the evidence in `data/manual-checks.json`), and `fail` (not published).

A passing URL proves the page exists, not that the description is right. Descriptions were written by comparing each against the repository's own description and README, or the page's title and text. Where a claim could not be found at the source, it was removed.

## API entries

`Auth` and `Limits` come from the provider's documentation, linked on each line. Where possible the auth claim was also tested with a keyless request:

| API | Keyless request | Result |
| --- | --- | --- |
| Europeana Record API | search without `wskey` | HTTP 401 |
| GeoNames | search without `username` | HTTP 401 |
| The National Archives (UK) Discovery | record details and search | HTTP 200 with JSON |
| WikiTree | `getProfile` with an `appId` | HTTP 200 |
| Open Archives | person search | HTTP 200 |
| Internet Archive | `advancedsearch.php` | HTTP 200 |
| Wikidata Query Service | query with a generic `python-requests` User-Agent | HTTP 403 |

The National Archives (US) Catalog API documents an `x-api-key` header issued by email and a default of 10,000 queries per month per key; a keyless request returns the website shell, not JSON.

The Discovery API of The National Archives (UK) publishes two different limits. The developer page gives a guideline of 3,000 calls per day at no more than one request per second. The fair-use policy sets a hard cap of 3,000 requests in any 5-minute period. The list shows both.

The FreeBMD terms of use allow only manual use of the search page and forbid front-end programs, so it appears in Research Guides with that warning and is not listed as an API.

Limits that the provider does not publish are written as "not verified" or "not published".

## Bot-blocked sites

Some sites (Gramps wiki, FHISO, ISOGG, SNPedia, GOV, FamilySearch wiki) answer automated requests with a challenge page. These are not counted as passes. Each has a note in `data/manual-checks.json` that says whether the check was a Wayback Machine snapshot whose text was read, or a web search that returned current pages from that site. A Wayback snapshot that was itself a bot wall was not accepted as evidence. Snapshots of the Gramps Data Model and FHISO Basic Concepts pages were that, so both entries were dropped; SNPedia was confirmed by web search instead.

FHISO's own front page lists no announcement newer than 2021 (reported by a second reviewer, not re-checked here). GEDCOM 7 is a FamilySearch standard, not a FHISO one; the FHISO entries describe FHISO's separate Extended Legacy Format draft.

## Comparison with existing lists

Compared on 2026-11-26 with [awesome-gedcom](https://github.com/todrobbins/awesome-gedcom), [lgg/awesome-genealogy](https://github.com/lgg/awesome-genealogy) and [Panda-Lewandowski/awesome-genealogy](https://github.com/Panda-Lewandowski/awesome-genealogy):

- **Overlap.** 48 of the 148 entries here also appear in at least one of them. Each was re-verified by the same pipeline instead of copied; 100 entries are new.
- **Freshness of the older lists.** Of the 40 GitHub repositories linked from awesome-gedcom, 12 were pushed to in the last 24 months, 2 are archived, 1 no longer exists and 15 have had no push for more than 60 months. Of the 38 in lgg/awesome-genealogy, 34 were active, 1 is archived and 1 no longer exists.
- **Breadth.** The older lists cover GEDCOM parsers and consumer sites. They have no entries for record-archive APIs with auth and limits, handwriting recognition engines and ground-truth data, historical gazetteers, record linkage and name parsing, JSON and RDF schemas, or standards such as EDTF, IIIF, ALTO, PAGE-XML and TEI.
- **Dropped on purpose.** Consumer research sites with no developer surface, archived repositories, and repositories untouched for more than five years.

## Keeping it fresh

`.github/workflows/verify.yml` re-runs the verification every week. If any entry fails it opens an issue with the failures; if only metadata changed (last-push months, license) it opens a pull request with the regenerated README. `.github/workflows/ci.yml` runs the tests and every linter on each push.

## Known limits

- Rate limits for FamilySearch, Geni, Trove, DPLA, IPUMS and Europeana were not found in the documentation read; the entries say so.
- A repository's last push is a proxy for maintenance. A commit that only bumps a dependency counts the same as a feature.
- Wayback and web-search evidence for bot-blocked sites shows the page exists, not that it is up right now.
- Only the eight GEDCOM libraries in [SMOKE-TESTS.md](SMOKE-TESTS.md) were run against a real file. The other parser, converter and visualization entries are verified by repository status and README, not by execution.
