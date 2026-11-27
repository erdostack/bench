# Jobs

- `run(conn)` gets a connection to the live database; return a count for the job log.
- The monitor and the customer dashboards read all day: at most 2,000 changed rows per transaction.
