-- Timetable, loaded every night from the schedule feed. All times are UTC, 'YYYY-MM-DD HH:MM'.
CREATE TABLE airport (
  code    TEXT PRIMARY KEY,   -- IATA
  name    TEXT NOT NULL,
  country TEXT NOT NULL
);

CREATE TABLE flight (
  id        INTEGER PRIMARY KEY,
  carrier   TEXT NOT NULL,
  flight_no TEXT NOT NULL,
  origin    TEXT NOT NULL REFERENCES airport(code),
  dest      TEXT NOT NULL REFERENCES airport(code),
  dep_utc   TEXT NOT NULL,
  arr_utc   TEXT NOT NULL
);

CREATE INDEX flight_by_origin ON flight (origin, dep_utc);
CREATE INDEX flight_by_dest ON flight (dest, dep_utc);
