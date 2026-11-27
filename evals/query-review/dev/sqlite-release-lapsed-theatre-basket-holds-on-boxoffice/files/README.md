# playhouse-tickets

Ticketing for the Harbour Lane Playhouse (a 640-seat town theatre and its 90-seat studio): performances,
patrons, staff, and the edges between them (who booked which seat, which seats are held and by whom).

- `bin/bo <target> "<sql>"` or `bin/bo <target> --file <file.sql>`: run SQL on a target.
- `bin/apply <target> changes/<file>.sql`: apply a change file (see `docs/changes.md`).
- `config/targets.toml`: the targets. `docs/targets.md` says what each one is.
- `docs/seats.md`: bookings and holds.
