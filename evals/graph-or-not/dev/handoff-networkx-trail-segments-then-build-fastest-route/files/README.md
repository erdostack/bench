# trailmate

API behind the hut association's walking app: trail info, hut opening times, and (soon) route suggestions.

- Python 3.12, Flask, one VM. `requirements.txt`.
- Trail data is a SQLite file (`var/trails.db`) exported from the survey team's GIS every Monday; not committed.
  Tables in `db/schema.sql`.
