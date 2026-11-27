# Jobs

- A job is a module in `jobs/` with `run(conn)`; it gets a connection to the live database.
- The scheduler starts each job at 01:00. When a job exits non-zero it is started again at every
  following slot (02:00, 03:00, ...) until it exits 0, so a job can run several times over the same data.
- Hydraulic modelling reads the network around the clock: at most 1,000 changed rows per transaction.
