Still stands: no

We decided no-graph because classes were flat: one join, 4 ms p95 against the 200 ms the check gets. With classes
nesting up to 5 levels, each drug now has up to 5 ancestor classes to match rules against, which is a walk. The
sizes still say small: 21k drugs and 140k rules, loaded once a month. So: compute each drug's ancestor classes in the
service when the monthly formulary load runs (21k drugs times at most 5 levels is about 100k entries), and keep
matching rules in SQL. I've updated ADR 0004 and docs/graph/DECISION.md to in-process-library. Still no case for the
vendor's graph database at 3,000 checks a minute.
