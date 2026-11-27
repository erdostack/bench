# netplan

Planning tools for the tram network. Analysts run these; nothing here serves riders.

- Python 3.12. `requirements.txt` lists what we use.
- The planning database is SQLite (`var/planning.db`, copied from the timetable export each night, not committed).
  Tables are in `db/schema.sql`.
- `python -m netplan.report` writes the nightly planning report to `var/report.md`.

## Layout

    db/schema.sql        tables of the planning database
    netplan/db.py        connection helper
    netplan/report.py    the nightly report
