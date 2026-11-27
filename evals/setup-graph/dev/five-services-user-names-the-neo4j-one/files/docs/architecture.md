# Architecture notes

_Last full review: when routing went live. Individual sections may be older._

## Why a graph database at all

Route planning is shortest-path work over a depot network that changes every night. We tried it in PostgreSQL
first; the recursive queries were correct and too slow. Memgraph keeps the whole network in memory and answers a
depot-to-depot query in a few milliseconds.

## One graph for everything

The plan is to keep a single graph database on the platform. Reporting lineage ("this number in the monthly
report came from these tables through these jobs") is also a graph problem, and the lineage service will store its
graph in the same Memgraph instance as routing, in a separate label namespace (`Lin*`), so that operations has one
engine to run and one backup to take.

## Service boundaries

- The gateway owns no data.
- Accounts is the only service that talks to PostgreSQL.
- Routing owns the depot network graph.
- Notifier keeps short-lived state in Redis and nothing else.

## Things we decided not to do

- No shared ORM models between services.
- No cross-service database access. If you need another service's data, call its API.
