# Jobs

- `run(conn)` gets a connection to live; return a count for the log.
- The planner reads `route_links` all the time: at most 500 changed rows per transaction.
