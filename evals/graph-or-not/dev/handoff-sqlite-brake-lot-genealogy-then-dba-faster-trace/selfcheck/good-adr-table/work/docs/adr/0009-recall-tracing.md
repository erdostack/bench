# ADR 0009: recall tracing on a graph database

Status: accepted

Decision: graph-database

The OEM contract allows 30 seconds for the containment list and for the backward trace. Postgres, tuned:
14 minutes forward. Graph database trial: 1.2 s / 0.9 s. Hosts are capped at 64 GB, so memory is out.
