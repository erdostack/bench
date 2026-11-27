# interlock

Board interlocks among listed companies, from the registry's public filings: people, companies and the
board seats between them. Analysts ask which companies are linked through shared directors and how far
apart two boards are.

## The graph

Neo4j 2026.08.1, started with `make up` (compose.yaml). Since 2026.06 a new deployment defaults to
Cypher 25, so everything in `queries/` is written for Cypher 25; see docs/QUERIES.md.

    make up
    make q F=queries/shared_directors.cypher COMPANY=C-00881

Logins are in `.env` (copy `.env.example`). The filings are loaded by the registry import job, which owns
writes.
