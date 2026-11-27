# paperlib

Reading-list graph for the lab. LadybugDB, embedded: one database file on the lab workstation, opened by the
desktop app, one writer at a time.

`db/schema.cypher` holds the table definitions and is run once on an empty database.

About 60,000 papers, 85,000 authors, 900,000 citations and 400 topics. Imports are a weekly batch; the rest is
people browsing.

What the app asks:

- a paper by DOI, an author by ORCID, a topic by slug
- an author's papers in order, and a paper's authors in byline order
- who cites a paper, and which papers are cited together with it
- a reading list for a topic, newest first
