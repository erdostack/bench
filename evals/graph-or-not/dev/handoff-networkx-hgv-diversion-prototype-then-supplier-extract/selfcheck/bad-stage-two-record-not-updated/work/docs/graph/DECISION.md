# Permit diversion checker: where the road network lives

Decision: need-more-information

## Workload facts (from the conversation, 2026-11-24)

- Worker: hard 1.5 GB limit; 2 s per check; about 300 checks a day.
- County sample: 38,000 segments, about 70 MB, 30 ms a route. National product: about 4 million segments.
- Missing: the segment count of the regional extract.

## Options considered

- graph-database (Dan): not before the size is known.
- in-process-library: fits up to roughly 15 times the sample.

## What would change the decision

- The extract's segment count.
