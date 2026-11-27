# Timetable

`connections` holds one row per train per pair of consecutive stops: `trip_id`, `seq` (1 for the first
leg of the trip), `from_station`, `to_station`, `dep` and `arr` as `HH:MM` text, exactly as the
national timetable feed publishes them. The importer adds the next week's rows every night.

Times are on the service day of the trip, as in the feed. A trip belongs to the day it starts on,
so a train that leaves at 23:40 and reaches the coast at 00:55 is published as `23:40` to `24:55`,
and the last sleeper calls at stops up to `27:20`. A trip never has a time earlier than the one
before it.

Stations: `stations(id, code, name)`.
