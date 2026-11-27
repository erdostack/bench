# Jobs

- `run(conn, ...)` gets a connection to live and returns a count for the job log.
- The optimiser and the planning UI read `lanes` around the clock: at most 2,000 changed rows per
  transaction.
- The scheduler kills a job that runs past its slot or loses its connection, and starts it again from
  the top in the next slot, with the same arguments.
