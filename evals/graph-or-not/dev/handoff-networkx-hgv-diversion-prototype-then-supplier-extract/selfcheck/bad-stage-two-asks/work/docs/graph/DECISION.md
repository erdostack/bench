# Permit diversion checker: where the road network lives

Decision: need-more-information

## Workload facts

- From the first conversation (2026-11-24): the worker has a hard 1.5 GB memory limit on the permit platform; a
  check must return within 2 s; about 300 checks a day. County sample: 38,000 segments, about 70 MB in the
  prototype, 30 ms a route. National product: about 4 million segments.
- Delivered (2026-11-24): the regional extract is 180,000 segments and 150,000 junctions.

## Options considered

- in-process-library: chosen. 180,000 segments is about 4.7 times the sample: roughly 330 MB, well inside 1.5 GB.
- graph-database (Dan): rejected; a server for 300 checks a day on a network that fits in the worker.
- recursive-sql: weighted quickest paths are not a recursive query.
- need-more-information: was the call until the extract's size was known.

## What would change the decision

- The extract growing past roughly 15 times the sample (about 570,000 segments), or the worker limit shrinking.
