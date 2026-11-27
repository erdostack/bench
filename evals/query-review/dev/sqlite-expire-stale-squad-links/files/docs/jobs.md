# Jobs

`run(conn)` gets a connection to the live database and returns a count for the log. Matchmaking reads
and writes the same file: no transaction may change more than 2,000 rows.
