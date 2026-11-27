# Flattening redirect chains for the nginx map

Decision: in-process-library

## Workload facts (given by the owner, 2026-11-23)

- `redirect`: 1.9M rows. Longest chain found by the SEO audit: 6 hops.
- Loops exist: 214 found, mostly a product renamed and renamed back.
- Agreed with SEO: a URL whose chain goes round a loop is left out of the map entirely (it 404s and the content
  team fixes it by hand). Do not pick a member of the loop.
- The nightly job has a one hour window and takes 4 minutes today.

## Options considered

- graph-database (Ravi's proposal): rejected. A store to load nightly for a batch walk of at most 6 hops.
- in-process-library: chosen. Read the table into a dict in the job and walk it with a visited set (a plain dict is
  enough; no library needed).
- recursive-sql: fine too; a recursive query that carries the visited path. Not chosen only because the loop rule
  reads more plainly in Python.
- no-graph: rejected. Chains are up to 6 hops.

## What would change the decision

- The job no longer fitting its hour, or the table no longer fitting comfortably in the jobs host's memory.
