# Impact analysis: requirements

Agreed with the analytics engineering leads, 2026-06. Supersedes the 2025 pilot notes.

## Granularity

Column. The question is "if I drop or retype `orders.amount`, which downstream columns, models and
dashboards are affected?". The 2025 pilot answered at table level and was rejected: wide staging tables
make almost everything depend on almost everything, so the answer was useless for review.

Each edge carries the job that produced it, the transformation expression and when it was last seen;
reviewers read those.

## Who asks

- `trailmark check` in CI: about 5,200 runs a day. It blocks a merge when a changed column has
  downstream consumers that the pull request does not touch.
- The web UI: about 300 analytics engineers.

## Freshness

A job that finished more than 60 seconds ago must be reflected. People merge, the pipeline runs, and
the next pull request has to see the new columns; stale answers produce both false blocks and missed
ones.

## Response time

p95 under 2 seconds for the CI check.
