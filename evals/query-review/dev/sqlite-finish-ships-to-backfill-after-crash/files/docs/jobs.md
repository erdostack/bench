# Jobs

- Jobs run against live; the intake planner reads the graph while they run.
- At most 2,000 changed rows per transaction.
- `run(conn)` returns a count for the job log.
- A job that stops part-way is run again the next night by the scheduler, with the same code.
