# kilbride-netinv

Network inventory tooling for the Kilbride and Auchen community fibre co-operative: exchange-hut OLTs,
the premises each PON port serves, and the core uplinks.

- `bin/ni "<sql>"` or `bin/ni --file <file.sql>`: run SQL on netinv (see `config/netinv.toml`).
- `bin/apply changes/<file>.py`: apply a change file to netinv (calls its `run(conn)`).
- `docs/DATA.md`: where the data lives and how it is changed. `docs/model.md`: tables and edges.
