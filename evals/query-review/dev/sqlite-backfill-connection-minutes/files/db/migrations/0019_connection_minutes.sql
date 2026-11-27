-- Integer times for the connection scan (RP-311). Filled by a job; NULL until then.
ALTER TABLE connections ADD COLUMN dep_min INTEGER;
ALTER TABLE connections ADD COLUMN arr_min INTEGER;
CREATE INDEX connections_from_min ON connections (from_station, dep_min);
