# tidepool

Back-office platform for a regional parcel carrier. One repository, five services, each owned by a small team and
deployable on its own.

| Service | What it does | Language | Data |
|---|---|---|---|
| `services/gateway` | public API, auth, rate limits | TypeScript | none |
| `services/accounts` | customers, contracts, invoices | Python | PostgreSQL 17 |
| `services/routing` | depot-to-depot route planning | Python | Memgraph 3.5 |
| `services/lineage` | where a figure in a report came from | Java | graph |
| `services/notifier` | email and SMS fan-out | Go | Redis |

## Graph database

The platform's graph database is Memgraph 3.5 (`memgraph/memgraph:3.5.0` in `compose.yaml`). Route planning needs
its in-memory traversals; see `docs/architecture.md` for why. Queries against it are run with `make mgq`.

## Running everything locally

    make up            # postgres, memgraph, redis
    make mgq FILE=services/routing/queries/next_hop.cypher
    make down

Each service has its own README with the commands for that service. Start there if you only work on one.
