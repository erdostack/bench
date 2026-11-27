# meshwatch

Monitoring for the neighbourhood mesh radio co-op. Relays are nodes and the radio links between them are
edges (`relay`, `link` tables); the link table is refreshed every five minutes by the poller.

- Links live in PostgreSQL 16 (compose.yaml); Redis keeps the alert de-duplication keys.
- Reachability questions ("which relays can still reach the uplink if R-07 goes down") are saved as recursive
  SQL in `queries/` and run with `make q F=queries/<file>.sql`.

```
make up
make q F=queries/reachable_from_uplink.sql
```
