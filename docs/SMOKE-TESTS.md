# Smoke tests

On 2026-11-26 each library below was installed from its registry and run once against the three-person fixtures in `tests/fixtures/` (`sample-5.5.1.ged`, and `sample-7.0.ged`, the same data with a 7.0 header). The check was: parse the file, read Ada Lovelace's name, her birth date and place where the API offers them, and count the individuals (3). A pass means the call succeeded and returned the expected values; it says nothing about large or malformed files.

| Library | Version | File | Result |
| --- | --- | --- | --- |
| ged4py | 0.5.5 | 5.5.1 | Pass: name, `10 DEC 1815`, `London, England`, 3 individuals, family links |
| python-gedcom | 1.1.0 | 5.5.1 | Pass: name, birth date and place, 3 individuals |
| gedcom7 (python-gedcom7 repository) | 1.4.0 | 7.0 | Pass: `loads` returned 6 records and `validate` is present; `dumps` writes a byte order mark, which GEDCOM 7 allows, and is otherwise identical |
| gedcom (tmcw) | 3.0.9 | 5.5.1 | Pass: JSON tree with 6 top-level records |
| read-gedcom | 0.3.2 | 5.5.1 | Pass: 3 individuals, name, birth year 1815 |
| @thememorypalace/gedcom-tools | 0.1.0 | 5.5.1 | Pass: `convertTo7` produced a 7.0 header and a conversion report |
| gedcom-go | 1.2.0 | 5.5.1 | Pass: decode without error, 3 individuals |
| elliotchance/gedcom | v39 | 5.5.1 | Pass: name, birth date and place |

Findings:

- The Python package for the `python-gedcom7` repository is published as `gedcom7`, not `python-gedcom7`.
- The `gedcom-tools` repository's `package.json` says 0.1.1, but npm's latest is 0.1.0, and installing from GitHub gives source without a built `dist`. Install from npm.
- The other parser, converter and visualization entries were not executed.

Re-run these checks by hand: install the packages above and call each with the fixture.
