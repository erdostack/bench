# morgue

The archive tool of a local newsroom: every article and podcast episode we have published since 2004, who
made it and what it is about. The database is LadybugDB, embedded in the archive service: one database file
on the archive server, opened by that one process, which answers the desk tool and runs the nightly import.

    db/schema.cypher    the table definitions, run once on an empty database
    db/queries.cypher   what the desk tool runs; each query has a `// name:` line
    docs/decisions.md   why the schema looks the way it does

About 240,000 articles, 6,500 episodes, 900 staff and contributors, 31,000 tags (people, places,
organisations and topics). An item has a dozen tags on average.

The desk tool's searches: everything with a tag, newest first; everything by a person; the tags of an item;
tags that often appear together with a given tag; and one item by its id or slug.
