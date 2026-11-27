# railnet-capacity

Train path capacity for the Wenlock & Severn freight network: timetable paths, the operators and
customers holding them, and the routes they run over, as a graph in `nodes` and `edges` (SQLite).

- `bin/rn "<sql>"` or `bin/rn --file <file.sql>`: run SQL on railnet.
- `bin/job jobs/<file>.py`: run a data job (calls its `run(conn)`) on railnet.
- `jobs/`: data jobs. `db/schema.sql`: the schema. `docs/`: how railnet is run, the model.
