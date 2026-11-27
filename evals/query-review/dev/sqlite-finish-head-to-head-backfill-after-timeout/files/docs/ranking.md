# Ranking

The ranking counts wins and losses from `meetings`, one row per played match (walkovers and retirements
before a ball was struck have `status = 'walkover'` and do not count). A match that appears twice in
`meetings` counts twice.

`meetings` was introduced in November 2026. `jobs/backfill_meetings.py` fills it from `matches` for
everything played so far; the results app writes new meetings itself from 2026-11-23 on.
