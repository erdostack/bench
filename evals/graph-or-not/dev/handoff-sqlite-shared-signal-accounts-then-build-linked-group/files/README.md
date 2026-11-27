# forum-mod

Moderation tools for the community forum: reports, bans, appeals, and the "linked accounts" panel moderators use
to spot ban evasion.

- Python 3.12, SQLite (`var/forum.db` on the moderation host, a nightly copy of production; not committed).
  Tables in `db/schema.sql`.
- networkx is installed for the abuse dashboard charts.
