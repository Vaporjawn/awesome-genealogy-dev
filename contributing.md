# Contributing

Thanks for helping keep this list accurate. It is built from data, so a contribution is a change to `data/entries.json` plus a rebuild.

## What belongs here

An entry must help someone who writes genealogy or family-tree software, and it must be one of:

- a specification, format or schema (GEDCOM, GEDCOM X, JSON, RDF, XML);
- a library, parser, converter, visualizer or tool with a public repository or documentation;
- a record, archive, gazetteer or DNA API or dataset a developer can call or download;
- an open-source genealogy application whose code others can read or extend.

It does not belong here if it is a commercial research site with no developer surface, a tutorial for researching your own tree, or a repository that is archived or that has had no push for more than 60 months.

## Adding an entry

1. Add an object to `data/entries.json`: `section`, `sub`, `name`, `url`, `desc`, and for GitHub projects `repo` (`owner/name`).
2. Write `desc` as one sentence that starts with a capital letter and ends with a period. Restate what the project says about itself; do not add claims you did not read. Do not repeat the name.
3. For an API, add `api` with `auth`, `limits` and `evidence` (the documentation page you read). Write "not verified" when you could not find the number. Check auth yourself with a keyless request when you can.
4. Run `python3 scripts/verify.py --only <id>` for the new entry. It must come back `pass`, or `manual` with a note in `data/manual-checks.json` explaining how you checked it by hand.
5. Run `python3 scripts/build_readme.py`, then `npm run lint`.
6. Open a pull request. List the sources you used for the description and any API facts.

Entries with `"keep": true` are older repositories (last push 24 to 60 months ago) retained as stable references. Say why in your pull request.

## Removing or correcting an entry

Open an issue or pull request with the evidence: the archived banner, the dead URL, or the documentation page that contradicts the entry. The weekly verification workflow also opens an issue when an entry fails.

## Style

- Alphabetical order is not required; entries within a sub-section go from most to least relevant.
- Use US spelling and plain language. No marketing words.
- One link per entry. Link the project, not an article about it.
