# Jobs

- `run(conn)` gets a connection to the live database and returns a count for the job log.
- The planner and the signs read the database all the time: a job commits at most 2,000 changed rows
  per transaction, counted over all tables.
