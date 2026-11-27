# Changelog

## 0.6.0 - 2026-07-30
- queries/ rewritten with the CYCLE clause of recursive queries (PostgreSQL 14 and later) instead of the
  hand-built path arrays; the mesh has loops everywhere and the old guard was easy to get wrong.

## 0.5.2 - 2026-06-11
- Local stack: deploy/local.env pins the database to the same major as the co-op's hosted instance.

## 0.5.0 - 2026-04-02
- Poller writes link quality as `snr_db`.
