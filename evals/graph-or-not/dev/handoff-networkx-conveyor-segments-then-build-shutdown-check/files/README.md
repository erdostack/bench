# linewatch

Line status board for the assembly hall: which stations are running, blocked or down.

- Python 3.12. The layout (stations and conveyor segments) is a SQLite file kept by line engineering
  (`var/layout.db`, schema in `db/schema.sql`).
- Status events come from the PLC gateway.
