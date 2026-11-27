# Data

## Tables

- `station(id, name, depth_m, survey_trip)`: one row per survey station.
- `passage(id, from_station, to_station, length_m, bearing, inclination)`: one measured shot.

## Integrity

`passage.from_station` and `passage.to_station` are foreign keys to `station(id)`, and `sql/schema.sql`
switches SQLite's foreign-key enforcement on before it creates the tables. So the database refuses a
passage to a station that does not exist, and refuses to delete a station that passages still use.
Queries can join passages to stations without guarding against missing rows.

## Merging duplicate stations

Two trips sometimes survey the same point under two ids. `make merge` deletes the duplicates listed in
`data/duplicates.csv`; any passage still using one would block the delete (see above).
