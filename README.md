# Awesome Genealogy Dev [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> Libraries, formats, APIs and tools for developers building genealogy and family-tree software.

This list is for people who write genealogy software, not for people researching their own tree. Search it on the [website](https://vaporjawn.github.io/awesome-genealogy-dev/) or read it below; both come from the same verified data. Looking for a GEDCOM parser, a family tree chart library, a FamilySearch or WikiTree API client, or a way to read old handwritten records? It is here. It covers file formats and specs, parsers, chart libraries, open-source apps, record-archive APIs, DNA and record-linkage tooling, handwriting recognition, historical geocoding, schemas and standards.

Looking for a GEDCOM parser, a GEDCOM 7 or GEDCOM X library, a family tree chart library for JavaScript or Python, a genealogy API (FamilySearch, WikiTree, Geni, national archives), a DNA segment or kinship tool, handwriting recognition for historical records, or a historical gazetteer? Each is a section below, and each API entry states its auth and rate limits.

Every one of the 148 entries was checked against the live web on 2026-11-26: the URL answers, GitHub repositories are not archived, and descriptions restate what the project or page says about itself. [How entries are verified](docs/METHODOLOGY.md) and how this list differs from the older GEDCOM and genealogy lists are written down.

How to read an entry:

- *Italic notes* after a repository give its license and the month of its last push. "Low activity" means no push for more than 24 months; those entries stay only as stable references.
- **Auth** and **Limits** on API entries come from the provider's own documentation, linked as "source". When a limit could not be found, the entry says "not verified" or "not published" instead of guessing.
- "Checked by hand, bot-blocked" means the site refuses automated requests, so the entry was confirmed another way; the evidence is in [data/manual-checks.json](data/manual-checks.json).
- There is no single standard called "GENEALOGY JSON". The Data Formats section lists the real JSON options and says how mature each one is.

## Contents

- [Data Formats](#data-formats)
- [Parsers and Converters](#parsers-and-converters)
- [Tree Visualization Libraries](#tree-visualization-libraries)
- [Genealogy Apps (Open Source)](#genealogy-apps-open-source)
- [Record and Archive APIs](#record-and-archive-apis)
- [DNA and Matching Tools](#dna-and-matching-tools)
- [OCR and Handwriting Recognition for Records](#ocr-and-handwriting-recognition-for-records)
- [Geocoding and Historical Places](#geocoding-and-historical-places)
- [Data Models and Schemas](#data-models-and-schemas)
- [Standards and Specs](#standards-and-specs)
- [Research Guides](#research-guides)

## Data Formats

### GEDCOM 5.5.1

- [GEDCOM 5.5.1 Specification](https://gedcom.io/specifications/ged551.pdf) - Lineage-linked GEDCOM 5.5.1 specification (PDF), the version many tools still read and write.

### GEDCOM 7

- [FamilySearch GEDCOM 7.0 Specification](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html) - Current FamilySearch GEDCOM specification: container format, data types, structures and the GEDZIP file format.
- [FamilySearch/GEDCOM](https://github.com/FamilySearch/GEDCOM) - Source repository of the GEDCOM 7 specification, including YAML term definitions for the gedcom.io namespace. *Apache-2.0, last push 2026-11.*
- [GEDCOM Registries](https://github.com/FamilySearch/GEDCOM-registries) - Registry of GEDCOM concepts and extension URIs, with a lookup table from URI to registry file. *no license, last push 2026-11.*
- [GEDCOM Migration Guide](https://gedcom.io/migrate/) - FamilySearch guide to migrating from GEDCOM 5.5.1 to 7.0.
- [gedcom.io Tools](https://gedcom.io/tools/) - FamilySearch list of tools for GEDCOM.

### GEDCOM X

- [GEDCOM X](http://www.gedcomx.org/) - Home of the GEDCOM X data model and serialization formats.
- [FamilySearch/gedcomx](https://github.com/FamilySearch/gedcomx) - Open data model and serialization format specifications for exchanging genealogical data. *Apache-2.0, last push 2026-04.*

### GENEALOGY JSON

- [GEDCOM X JSON Serialization](https://github.com/FamilySearch/gedcomx/blob/master/specifications/json-format-specification.md) - Specification of the JSON serialization of the GEDCOM X model.
- [AXGF Specification](https://github.com/plkarin/axgf-spec) - Very new open spec for a JSON-native genealogy exchange format with confidence scoring; unproven outside its own repository. *CC0-1.0, last push 2026-11.*
- [gedcom (tmcw)](https://github.com/tmcw/gedcom) - JavaScript parser and CLI that translates GEDCOM structure into JSON. *ISC, last push 2025-12.*
- [gedcom.json](https://github.com/Jisco/gedcom.json) - Converts GEDCOM files to a JSON file or JavaScript object and back. *MIT, last push 2026-03.*

### Other

- [Gramps XML](https://gramps-project.org/wiki/index.php/Gramps_XML) - XML format designed for storing Gramps data in a portable, human- and machine-readable form. *checked by hand, bot-blocked.*
- [FHISO Extended Legacy Format](https://fhiso.org/TR/elf-serialisation) - FHISO exploratory draft of a GEDCOM-compatible serialisation format with a structured extensibility mechanism. *checked by hand, bot-blocked.*

## Parsers and Converters

### JavaScript and TypeScript

- [read-gedcom](https://github.com/arbre-app/read-gedcom) - Typed GEDCOM parser written in TypeScript. *MIT, last push 2025-12.*
- [gedcom-tools](https://github.com/thememorypalace/gedcom-tools) - Converts GEDCOM 5.5.1 to 7.0 and back, checks files and decodes ANSEL, with no dependencies; published on npm as @thememorypalace/gedcom-tools. *MIT, last push 2026-11.*
- [gedcom-test-files](https://github.com/thememorypalace/gedcom-test-files) - Small synthetic GEDCOM 5.5.1 and 7.0 files with known faults and encoding edge cases for testing parsers. *MIT, last push 2026-11.*
- [JsGEDCOM](https://github.com/MesseBasseProduction/JsGEDCOM) - JavaScript GEDCOM parser. *GPL-3.0, last push 2026-06.*

### Python

- [python-gedcom7](https://github.com/DavidMStraub/python-gedcom7) - Python parser and serializer for GEDCOM 7. *MIT, last push 2026-11.*
- [ged4py](https://github.com/andy-z/ged4py) - Python parser for GEDCOM 5.5.1 that reads UTF-8, ASCII and ANSEL and is designed for large files. *MIT, last push 2026-09.*
- [python-gedcom](https://github.com/madprime/python-gedcom) - Python module for parsing, analyzing and manipulating GEDCOM files. *GPL-2.0, last push 2024-01, low activity.*

### Java and Kotlin

- [gedcom5-java](https://github.com/FamilySearch/gedcom5-java) - FamilySearch Java parsers for GEDCOM 5. *Apache-2.0, last push 2026-10.*
- [gedcom4j](https://github.com/frizbog/gedcom4j) - Java library for reading and writing GEDCOM 5.5 and 5.5.1 files. *no license, last push 2023-06, low activity.*
- [gedcomx-java](https://github.com/FamilySearch/gedcomx-java) - Java support for GEDCOM X. *Apache-2.0, last push 2026-10.*

### Go

- [gedcom (elliotchance)](https://github.com/elliotchance/gedcom) - Go library and CLI tools for encoding, decoding, traversing, merging, comparing, querying and publishing GEDCOM files. *MIT, last push 2026-11.*
- [gedcom-go](https://github.com/cacack/gedcom-go) - Lossless Go library for reading, writing, validating and converting GEDCOM 5.5, 5.5.1 and 7.0. *MIT, last push 2026-11.*

### Rust

- [gedcomx-rs](https://github.com/ephraimkunz/gedcomx-rs) - Collection of Rust crates for working with GEDCOM X. *MIT, last push 2026-06.*
- [rust-gedcom](https://github.com/pirtleshell/rust-gedcom) - Rust GEDCOM parser with an optional serde JSON feature. *MIT, last push 2023-01, low activity.*

### .NET

- [GeneGenie.Gedcom](https://github.com/TheGeneGenieProject/GeneGenie.Gedcom) - .NET library for loading, saving and analyzing GEDCOM family trees. *AGPL-3.0, last push 2026-11.*
- [gedcomx-csharp](https://github.com/FamilySearch/gedcomx-csharp) - C# libraries for processing GEDCOM X. *Apache-2.0, last push 2023-04, low activity.*

### PHP

- [magicsunday/gedcom-parser](https://github.com/magicsunday/gedcom-parser) - Streaming GEDCOM 5.5.1 and 7.0 parser for PHP 8.3+ with a fully typed model. *MIT, last push 2026-11.*
- [php-gedcom](https://github.com/liberusoftware/php-gedcom) - Reading and writing GEDCOM 5.5.1 and GEDCOM X for PHP 8.4. *MIT, last push 2026-07.*

### Dart and Ruby

- [gedcom-dart](https://github.com/orestesgaolin/gedcom-dart) - Dart library to parse GEDCOM data. *GPL-2.0, last push 2026-07.*
- [gedcom (rbur004)](https://github.com/rbur004/gedcom) - Ruby GEDCOM parser. *no license, last push 2022-04, low activity.*

### Converters

- [ged2dot](https://github.com/vmiklos/ged2dot) - Converts GEDCOM to Graphviz DOT. *MPL-2.0, last push 2026-11.*
- [gedcom5-conversion](https://github.com/FamilySearch/gedcom5-conversion) - FamilySearch utilities for converting GEDCOM 5.5 to GEDCOM X. *no license, last push 2024-04, low activity.*
- [ged2site](https://github.com/nigelhorne/ged2site) - Creates a family-tree website from a GEDCOM file; written in Perl. *GPL-2.0, last push 2026-11.*
- [GEDCOM to Visual Map](https://github.com/D-Jeffrey/gedcom-to-visualmap) - Builds Folium or KML maps from GEDCOM data, geocoding the places it finds. *MIT, last push 2026-09.*
- [gedcom-cli](https://github.com/cacack/gedcom-cli) - Command-line tool for inspecting, validating and correcting GEDCOM files, built on gedcom-go. *MIT, last push 2026-11.*

## Tree Visualization Libraries

### JavaScript and D3

- [family-chart](https://github.com/donatso/family-chart) - Family-tree visualization built on D3, with tree filtering, card variants and code generation for React, Vue, HTML and JSON. *MIT, last push 2026-04.*
- [topola](https://github.com/PeWu/topola) - Library that renders genealogy charts as SVG: ancestors, descendants, hourglass and relatives. *Apache-2.0, last push 2026-11.*
- [dTree](https://github.com/ErikGartner/dTree) - D3 library for visualizing data trees with multiple parents, such as family trees. *MIT, last push 2024-05, low activity.*
- [d3-dag](https://github.com/erikbrinkman/d3-dag) - Layout algorithms for directed acyclic graphs, which fit family trees where people have several partners. *MIT, last push 2026-11.*
- [relatives-tree](https://github.com/SanichKotikov/relatives-tree) - Calculates data for family-tree nodes and connectors from JSON. *MIT, last push 2025-03.*
- [react-family-tree](https://github.com/SanichKotikov/react-family-tree) - React component that renders a family tree. *MIT, last push 2024-07, low activity.*
- [PedigreeJS](https://github.com/CCGE-BOADICEA/pedigreejs) - Web tool for building pedigrees, from the CCGE-BOADICEA organization. *GPL-3.0, last push 2026-10.*
- [kingraph](https://github.com/rstacruz/kingraph) - Plots family trees from a YAML file to SVG using Graphviz. *no license, last push 2022-12, low activity.*

### Canvas and diagram engines

- [FamilyTreeJS](https://github.com/BALKANGraph/FamilyTreeJS) - Family-tree chart library by BALKAN; the repository carries no open-source license. *no license, last push 2026-08.*
- [GoJS Family Tree Sample](https://gojs.net/latest/samples/familyTree.html) - Family-tree diagram sample for the commercial GoJS diagramming library.
- [synergycodes/familyTree](https://github.com/synergycodes/familyTree) - Family-tree layout implemented with GoJS. *no license, last push 2025-06.*
- [Graphviz](https://graphviz.org/) - Graph layout software; GEDCOM tools such as ged2dot and kingraph render through it.

### Python and R

- [kinship2](https://cran.r-project.org/package=kinship2) - R routines for family data with a pedigree object, including kinship and identity-by-descent structures.
- [ggenealogy](https://cran.r-project.org/package=ggenealogy) - R tools for searching genealogical data and visualizing the results.
- [webtrees-pedigree-chart](https://github.com/magicsunday/webtrees-pedigree-chart) - SVG pedigree chart module for webtrees using D3.js with several layouts. *GPL-3.0, last push 2026-11.*

## Genealogy Apps (Open Source)

### Desktop

- [Gramps](https://github.com/gramps-project/gramps) - Source code of the Gramps genealogy program, written in Python. *GPL-2.0, last push 2026-10.*
- [Gramps Addons](https://github.com/gramps-project/addons-source) - Contributed third-party plugins for Gramps. *GPL-2.0, last push 2026-11.*
- [GEDKeeper](https://github.com/Serg-Norseman/GEDKeeper) - Cross-platform genealogy database; an MCP server plugin connects it to LLM clients. *GPL-3.0, last push 2026-11.*
- [Ancestris](https://www.ancestris.org/) - Free genealogy software for Windows, Mac and Linux that follows the GEDCOM standard.
- [Family Gem](https://github.com/michelesalvador/FamilyGem) - Android family-tree app that imports and exports GEDCOM. *GPL-3.0, last push 2026-10.*

### Web and self-hosted

- [Gramps Web](https://github.com/gramps-project/gramps-web) - Open-source online genealogy system built on Gramps. *AGPL-3.0, last push 2026-11.*
- [webtrees](https://github.com/fisharebest/webtrees) - Online collaborative genealogy application written in PHP. *GPL-3.0, last push 2026-11.*
- [GeneWeb](https://github.com/geneweb/geneweb) - OCaml genealogy software with a web interface; the engine behind large public databases such as Roglo. *GPL-2.0, last push 2026-11.*
- [Genealogy (MGeurts)](https://github.com/MGeurts/genealogy) - Laravel family-tree application for recording family members and their relationships. *MIT, last push 2026-11.*
- [Liberu Genealogy](https://github.com/liberu-genealogy/genealogy-laravel) - Genealogy and family-tree application built with Laravel, Filament and Livewire. *MIT, last push 2026-11.*
- [Genea](https://github.com/genea-app/genea-app) - Serverless browser app for viewing and editing GEDCOM family trees. *MIT, last push 2025-12.*
- [Betty](https://github.com/bartfeenstra/betty) - Builds interactive genealogy websites from Gramps and GEDCOM data. *GPL-3.0, last push 2026-11.*
- [giapha-os](https://github.com/homielab/giapha-os) - Family genealogy application for exploring family trees and managing members. *MIT, last push 2026-11.*

### Notes and plugins

- [Charted Roots](https://github.com/banisterious/obsidian-charted-roots) - Obsidian plugin with family charts, maps, PDF reports and GEDCOM or Gramps import and export. *MIT, last push 2026-08.*

## Record and Archive APIs

### Family trees

- [FamilySearch API](https://developers.familysearch.org/) - REST API with resources for genealogies, pedigree, names, search and match, and places, plus photos and stories. **Auth:** OAuth 2 access token; apps need approval and keys through a third-party service provider application. **Limits:** No charge; throttle values not published in the docs read. ([source](https://developers.familysearch.org/))
- [WikiTree API](https://github.com/wikitree/wikitree-api) - Documentation and examples for the WikiTree API. **Auth:** None for public profiles; login needed for private ones. **Limits:** Calls without an appId parameter face strict rate limits; numbers not published. ([source](https://github.com/wikitree/wikitree-api/blob/main/README.md)) *no license, last push 2026-09.*
- [Geni API](https://www.geni.com/platform/developer/help) - REST API with profile, union, document, photo, project and world-family-tree resources. **Auth:** OAuth 2 app registration. **Limits:** Per-app rate limit reported in X-API-Rate-Limit, X-API-Rate-Remaining and X-API-Rate-Window headers; values can change without notice. ([source](https://www.geni.com/platform/developer/help/rate_limits))
- [Gramps Web API](https://github.com/gramps-project/gramps-web-api) - RESTful web API for a Gramps database; the backend of Gramps Web. **Auth:** Controlled by your own deployment; see the Gramps Web API documentation. **Limits:** None imposed by a provider; you host it. ([source](https://gramps-project.github.io/gramps-web-api/)) *AGPL-3.0, last push 2026-11.*

### National and open archives

- [The National Archives Discovery API](https://discovery.nationalarchives.gov.uk/API/) - JSON API for the Discovery catalogue of The National Archives (UK). **Auth:** No key for the calls tested (record details and search returned 200); access is requested by email with the calling IP address, and an identifying User-Agent is required. **Limits:** Guideline of 3,000 calls per day at no more than 1 request per second; the fair-use policy sets a hard cap of 3,000 requests per 5 minutes and blocks the IP above it; content must not be cached. ([source](https://www.nationalarchives.gov.uk/help/discovery-for-developers-about-the-application-programming-interface-api/))
- [National Archives Catalog API](https://catalog.archives.gov/api/v2/api-docs) - NARA catalog API for archival descriptions, authority records, extracted text and digital object metadata. **Auth:** API key sent in the x-api-key header, requested by email. **Limits:** 10,000 queries per month per key by default, higher on request. ([source](https://github.com/usnationalarchives/Catalog-API/blob/master/README.md))
- [Library of Congress JSON API](https://www.loc.gov/apis/) - JSON and YAML API of loc.gov for digitized collections; Chronicling America has its own API page. **Auth:** None. **Limits:** 20 requests per minute on the JSON/YAML API, blocked for 1 hour when exceeded; text and image services allow 150 per minute. ([source](https://www.loc.gov/apis/json-and-yaml/working-within-limits/))
- [Open Archives API](https://www.openarchieven.nl/api/docs/) - Search API for the Open Archives genealogical search engine. **Auth:** None for most methods; methods marked with an asterisk need a key. **Limits:** 4 requests per second per IP address by default. ([source](https://www.openarchieven.nl/api/docs/))
- [Europeana APIs](https://apis.europeana.eu/) - Search, Record and IIIF APIs for digitized cultural heritage from European institutions. **Auth:** Free personal API key from a Europeana account (a keyless request returns 401). **Limits:** Usage limit enforced with HTTP 429; quota not verified. ([source](https://apis.europeana.eu/))
- [Trove API](https://trove.nla.gov.au/about/create-something/using-api) - National Library of Australia API for Trove content. **Auth:** API key after accepting the terms; needs a Trove account. **Limits:** Rate shown in your Trove account; not published on the page read. ([source](https://trove.nla.gov.au/about/create-something/using-api))
- [DPLA API](https://pro.dp.la/developers/api-codex) - API for metadata in the Digital Public Library of America. **Auth:** API key, appended as api_key to each request. **Limits:** Not verified. ([source](https://pro.dp.la/developers/api-codex))
- [Internet Archive Developer Portal](https://archive.org/developers/) - Developer portal for Internet Archive APIs covering item metadata, search, uploads and OCR. **Auth:** None for read calls tested; credentials needed for writes. **Limits:** Not verified. ([source](https://archive.org/developers/))

### Census and linked data

- [IPUMS API](https://developer.ipums.org/) - JSON API to define and download extracts from IPUMS data collections including NHGIS and IPUMS USA. **Auth:** API key from an IPUMS account. **Limits:** Not verified. ([source](https://developer.ipums.org/))
- [Wikidata Query Service](https://www.mediawiki.org/wiki/Wikidata_Query_Service/User_Manual) - SPARQL endpoint over Wikidata, handy for linking people and places. **Auth:** None; send a descriptive User-Agent (a generic python-requests User-Agent got HTTP 403 in a test). **Limits:** 60 second query deadline; 60 seconds of processing time per client per 60 seconds; HTTP 429 when throttled. ([source](https://www.mediawiki.org/wiki/Wikidata_Query_Service/User_Manual))

### AI access

- [Open Archives MCP Server](https://github.com/coret/openarchieven-mcp-server) - MCP server for the Open Archives genealogical search engine. *no license, last push 2026-10.*

## DNA and Matching Tools

### DNA tools

- [DNA Painter](https://dnapainter.com/) - Chromosome mapping and the Shared cM Tool for relationship probabilities.
- [GEDmatch](https://www.gedmatch.com/) - Upload and compare autosomal DNA kits from several testing companies.
- [Genetic Affairs](https://geneticaffairs.com/) - DNA match analysis tools for genetic genealogy.
- [ISOGG Wiki](https://isogg.org/wiki/) - Wiki of the International Society of Genetic Genealogy covering haplogroups, DNA projects and testing. *checked by hand, bot-blocked.*
- [YFull](https://www.yfull.com/) - Y-DNA and mtDNA interpretation service that publishes the YTree phylogeny.
- [Haplogrep 3](https://github.com/genepi/haplogrep3) - Free mtDNA haplogroup classification service, also offered as a web service. *MIT, last push 2026-06.*
- [Yleaf](https://github.com/genid/Yleaf) - Y-chromosomal haplogroup inference from next-generation sequencing data. *GPL-3.0, last push 2026-11.*
- [ped-sim](https://github.com/williamslab/ped-sim) - Program that simulates pedigree structures. *GPL-3.0, last push 2026-08.*
- [hap-ibd](https://github.com/browning-lab/hap-ibd) - Detects identity-by-descent segments in phased genotype data. *no license, last push 2024-06, low activity.*
- [PLINK 2](https://www.cog-genomics.org/plink/2.0/) - Toolkit for genotype data analysis.
- [SNPedia](https://www.snpedia.com/) - Wiki of human DNA variations that cites peer-reviewed studies; a separate bots.snpedia.com host serves automated access. *checked by hand, bot-blocked.*

### Record linkage and names

- [Splink](https://github.com/moj-analytical-services/splink) - Probabilistic record linkage with several SQL backends. *MIT, last push 2026-11.*
- [dedupe](https://github.com/dedupeio/dedupe) - Python library for fuzzy matching, record deduplication and entity resolution. *MIT, last push 2025-07.*
- [recordlinkage](https://github.com/J535D165/recordlinkage) - Modular Python toolkit for record linkage and duplicate detection. *BSD-3-Clause, last push 2024-02, low activity.*
- [jellyfish](https://github.com/jamesturk/jellyfish) - Python library for approximate and phonetic string matching. *MIT, last push 2026-10.*
- [python-nameparser](https://github.com/derek73/python-nameparser) - Parses human names into title, given, middle, family, suffix, nickname and maiden name. *no license, last push 2026-11.*

## OCR and Handwriting Recognition for Records

### Platforms

- [Transkribus](https://www.transkribus.org/) - Platform for text recognition, layout detection, model training, search and publishing, with a developer API.
- [eScriptorium](https://gitlab.com/scripta/escriptorium) - Open-source web platform for transcribing and segmenting historical documents.
- [OCR4all](https://github.com/OCR4all/OCR4all) - Provides OCR services through web applications. *MIT, last push 2026-09.*
- [FromThePage](https://github.com/benwbrum/fromthepage) - Wiki-like application for crowdsourcing transcription of handwritten documents. *AGPL-3.0, last push 2026-11.*

### Engines and models

- [Kraken](https://github.com/mittagessen/kraken) - OCR engine for all the languages. *Apache-2.0, last push 2026-11.*
- [Tesseract](https://github.com/tesseract-ocr/tesseract) - Open-source OCR engine. *Apache-2.0, last push 2026-11.*
- [Calamari](https://github.com/Calamari-OCR/calamari) - Line-based text recognition engine based on OCRopy. *GPL-3.0, last push 2026-06.*
- [Loghi](https://github.com/knaw-huc/loghi) - Toolkit for handwritten text recognition and OCR from the KNAW Humanities Cluster. *MIT, last push 2026-10.*
- [PyLaia](https://github.com/jpuigcerver/PyLaia) - Deep-learning toolkit for handwritten document analysis. *MIT, last push 2025-10.*
- [docTR](https://github.com/mindee/doctr) - Library for OCR-related tasks powered by deep learning. *Apache-2.0, last push 2026-11.*
- [TrOCR Handwritten](https://huggingface.co/microsoft/trocr-base-handwritten) - Transformer-based model for recognizing handwriting in single text-line images.

### Data and tools

- [HTR-United](https://htr-united.github.io/) - Catalogue of open ground-truth datasets for handwritten and printed text recognition.
- [Tropy](https://github.com/tropy/tropy) - Research photo management for archival photographs. *no license, last push 2026-11.*

## Geocoding and Historical Places

### Geocoders

- [GeoNames](https://www.geonames.org/export/web-services.html) - Gazetteer web services; every request needs a registered username. **Auth:** Free account; username parameter required on every request (a keyless call returns 401). **Limits:** 10,000 credits per day and 1,000 credits per hour per username on the free service. ([source](https://www.geonames.org/export/))
- [Nominatim Usage Policy](https://operations.osmfoundation.org/policies/nominatim/) - Rules for the public OpenStreetMap geocoder: identify your app and stay at or below one request per second. **Auth:** None; a valid Referer or User-Agent is required. **Limits:** Absolute maximum of 1 request per second, no heavy use. ([source](https://operations.osmfoundation.org/policies/nominatim/))
- [Photon](https://github.com/komoot/photon) - Open-source geocoder for OpenStreetMap data. *Apache-2.0, last push 2026-11.*
- [Pelias](https://github.com/pelias/pelias) - Modular open-source geocoder built on Elasticsearch. *MIT, last push 2026-07.*
- [geopy](https://github.com/geopy/geopy) - Geocoding library for Python. *MIT, last push 2026-07.*

### Historical gazetteers

- [World Historical Gazetteer](https://whgazetteer.org/) - Gazetteer linking historical place names, with a reconciliation API. **Auth:** API token required for most endpoints; a read-only MCP server exposes public place data without one. **Limits:** Reconciliation endpoint 600 queries per minute and 5,000 requests per day by default. ([source](https://docs.whgazetteer.org/content/technical/apis.html))
- [Pleiades](https://pleiades.stoa.org/) - Community-built gazetteer and graph of ancient places.
- [OpenHistoricalMap](https://www.openhistoricalmap.org/) - Interactive map of the world throughout history, dedicated to the public domain.
- [GOV Historical Gazetteer](https://gov.genealogy.net/) - Free online gazetteer of historical places and church affiliations run by the Verein fuer Computergenealogie. *checked by hand, bot-blocked.*
- [Getty Thesaurus of Geographic Names](https://www.getty.edu/research/tools/vocabularies/tgn/) - Getty Research Institute vocabulary of geographic names.

### Boundaries

- [Atlas of Historical County Boundaries](https://publications.newberry.org/ahcb/) - Newberry Library atlas of historical US county boundaries.
- [IPUMS NHGIS](https://www.nhgis.org/) - Historical US census tables and GIS boundary files from IPUMS.
- [A Vision of Britain through Time](https://www.visionofbritain.org.uk/) - Online library of British local history with maps and statistics.

## Data Models and Schemas

### Conceptual models

- [GEDCOM X Conceptual Model](https://github.com/FamilySearch/gedcomx/blob/master/specifications/conceptual-model-specification.md) - Conceptual model of the GEDCOM X data format.
- [Bio CRM](http://ldf.fi/schema/bioc/) - Ontology of biographical persons and their relations, published by Linked Data Finland.

### Vocabularies

- [schema.org Person](https://schema.org/Person) - Web vocabulary type with family properties such as parent, children, spouse and sibling.
- [Relationship Vocabulary](https://vocab.org/relationship/) - RDF vocabulary of relationship terms such as parentOf and grandparentOf.
- [FOAF](http://xmlns.com/foaf/spec/) - Linked-data vocabulary for people and their connections.

### Database schemas

- [SQLite Tools for RootsMagic](https://sqlitetoolsforrootsmagic.com/) - SQL queries for exploring a RootsMagic SQLite database.

## Standards and Specs

### Genealogy

- [FHISO](https://fhiso.org/) - Family History Information Standards Organisation, publisher of open family-history standards.

### Dates and text

- [Extended Date/Time Format](https://www.loc.gov/standards/datetime/) - Library of Congress specification for uncertain and approximate dates.
- [TEI Personography](https://tei-c.org/release/doc/tei-p5-doc/en/html/ND.html) - TEI Guidelines chapter on names, dates, people and places.

### Images and transcription

- [IIIF](https://iiif.io/) - International Image Interoperability Framework, image and presentation APIs for digitized objects.
- [W3C Web Annotation Data Model](https://www.w3.org/TR/annotation-model/) - W3C model for annotating web resources, including images and transcriptions.
- [ALTO XML](https://www.loc.gov/standards/alto/) - Library of Congress technical metadata schema for layout and text objects.
- [PAGE-XML](https://github.com/PRImA-Research-Lab/PAGE-XML) - PAGE XML format collection for document image page content. *Apache-2.0, last push 2026-01.*

### Archives

- [Encoded Archival Description](https://www.loc.gov/ead/) - Library of Congress site for the EAD standard for archival finding aids.
- [OAI-PMH](https://www.openarchives.org/pmh/) - Open Archives Initiative protocol for metadata harvesting.

## Research Guides

### Methods and standards

- [FamilySearch Research Wiki](https://www.familysearch.org/en/wiki/) - Free research guides covering places, record types and methods. *checked by hand, bot-blocked.*
- [Board for Certification of Genealogists Standards](https://bcgcertification.org/ethics-standards/) - BCG ethics and standards, including the Genealogical Proof Standard.
- [Genetic Genealogy Standards](https://www.geneticgenealogystandards.com/) - Ethical and usage standards for genetic genealogy.

### Developer reading

- [Modern Software Experience](https://www.tamurajones.net/) - Articles on GEDCOM versions, extensions and compatibility.
- [Gramps Developer Portal](https://www.gramps-project.org/wiki/index.php/Portal:Developers) - Portal for Gramps development, with pointers to source code, getting started and addon development. *checked by hand, bot-blocked.*

### Archives and places

- [GENUKI](https://www.genuki.org.uk/) - Reference library of UK and Ireland places and record sources.
- [Cyndi's List](https://www.cyndislist.com/) - Categorized directory of genealogy websites.
- [FreeBMD](https://www.freebmd.org.uk/) - Transcribed England and Wales civil registration births, marriages and deaths; its terms allow only manual use of the search page and forbid front-end programs.

Contributions are welcome; read [contributing.md](contributing.md) first. `README.md` is generated from `data/entries.json`, so change the data and rebuild instead of editing it by hand.
