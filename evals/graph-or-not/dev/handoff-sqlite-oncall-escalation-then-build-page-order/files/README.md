# pagerline

The paging side of our on-call tooling. The admin UI (separate repo) exports the escalation config to a SQLite
file (schema in `db/schema.sql`) and every pager node gets a copy on each change.

- `oncall/escalate.py`: who gets paged, and what happens when nobody acks.
- `oncall/notify.py`: formatting for pages.

Run things with Python 3.11+; there are no third-party dependencies.
