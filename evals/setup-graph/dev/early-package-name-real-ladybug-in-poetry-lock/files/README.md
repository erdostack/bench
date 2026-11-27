# bandtree

Who played with whom. A family tree of a (made-up) local music scene: musicians, bands, and who was in which band
when. The fun queries are the ones that hop: "which bands are two line-up changes away from The Quiet Lanterns?"

The graph is an embedded LadybugDB database, a single directory under `var/`. There is no server to start.

    poetry install
    poetry run python -m bandtree.load data/
    poetry run bandtree-ask queries/shared_members.cypher band="The Quiet Lanterns"

`bandtree-ask` opens the database read-only, so it is safe to point at the copy the website is built from.
