Added jobs/empty_trash.py. It deletes the cards trashed before 2026-10-24 (2,956 on the copy), and
first every connector and frame membership that has one of them at either end, found by card id: per
docs/model.md an arrow can be restored on its own, so 1,723 connectors on those cards have no
trashed_at, and memberships are never trashed. Deleting by trashed_at alone would have left them
pointing at deleted cards. Deletes go 1,000 rows per commit; returns 2,956.
