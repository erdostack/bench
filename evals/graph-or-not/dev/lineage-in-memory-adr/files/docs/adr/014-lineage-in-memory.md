# ADR 014: serve lineage from memory

**Status:** accepted · **Date:** 2026-09-22 · **Deciders:** platform data team

## Context

Impact queries run as recursive SQL over the lineage tables and are slow enough that people have
stopped waiting for them. We do not want to run another database.

## Decision

Each `lineage-api` pod loads the lineage graph into a NetworkX `DiGraph` at start-up and answers
upstream and downstream questions by walking it. Reload every 30 minutes.

## Sizing

The catalog has about 310,000 tables and 1.9 million table-to-table edges. A graph of that size is
comfortably under 2 GB in NetworkX, and the pods have 4 GB.

## Consequences

- `networkx` becomes a dependency; `lineage/loader.py` builds the graph.
- No new infrastructure.
- Results can be up to 30 minutes old.
