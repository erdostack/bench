# Jobs

`run(conn)` gets a connection to the live database and returns a count for the log. The app writes to
the same file: at most 1,000 changed rows per transaction.
