# galleria

Collection graph for a group of museums. Neo4j 5.

    graph/schema.cypher    constraints and indexes
    graph/load.cypher      nightly sync from the collections management system
    graph/queries.cypher   queries behind the public collection site; each has a `// name:` line

## The sync

The collections system exports everything every night: artworks, makers, who made what, and loans. The sync
replays the export through `load.cypher` with four workers in parallel, each sending batches of 2,000 rows as
`$rows`. An artwork is identified by its accession number (for example `1987.214.3`), which is what the export,
the labels on the wall and the public URLs all use.

## Size

| Thing | Count |
|---|---|
| `Artwork` | 1.9 million |
| `Maker` | 240,000 |
| `Venue` | 310 |
| `MADE_BY` | 2.3 million |
| `ON_LOAN_TO` | 85,000 |

`artwork_page` is the page behind every public artwork URL.
