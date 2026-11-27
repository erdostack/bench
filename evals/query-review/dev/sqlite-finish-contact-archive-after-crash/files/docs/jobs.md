# Nightly jobs

The nightly run starts at 03:00 against the live file while people keep messaging.

- `run(conn)` gets the connection. Return counts for the run log.
- Keep write transactions short: at most 1,000 changed rows per transaction.
- A job that dies is simply run again the next night.
