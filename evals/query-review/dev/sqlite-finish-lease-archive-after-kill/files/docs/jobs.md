# Jobs

- `run(conn)` gets a connection to the live database and returns a count for the log.
- At most 1,000 changed rows per transaction; the portal reads all night.
- The scheduler kills any job still running at 03:00 and starts it again the next night. A job has to
  be correct when it is killed at any point and run again.
