# murmur-jobs

Batch jobs for murmur, the short-post app. Each night at 02:00 the app's export task writes the follower graph to
`exports/` (not committed):

- `exports/accounts.txt`: every account id, one per line.
- `exports/follows.edges`: one follow per line, whitespace-separated; the header line names the columns.

Jobs live in `jobs/`, one module each, and run on the batch box from cron. Definitions of the scores the
product shows are in `docs/scores.md`.

Python 3.11+, networkx is installed on the batch box (see requirements.txt).
