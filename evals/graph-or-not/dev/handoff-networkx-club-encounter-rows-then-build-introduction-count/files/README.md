# clubhouse

Volunteer-run platform for community clubs: member pages, rotas, and the "who knows whom" pages for club
welfare officers. The demo club is Zachary's karate club (34 members), as bundled with networkx.

- Python 3.12, Flask, SQLite (`var/club.db`, built by `python -m club.load`, not committed).
- Tables in `db/schema.sql`. `encounter` has one row per context in which two members met.
- `club/graph.py` builds the networkx graph the stats page uses.
