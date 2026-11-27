Position: keep

We decided on recursive-sql (docs/adr/0003-circuit-trace.md): one recursive query instead of the 600 round
trips that make today's trace take 2.1 s. In memory the biggest variant was 45 MB and traced in 0.4 ms, so
the data is small and changes monthly; Neo4j would add a server for that.
