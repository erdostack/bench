CREATE TABLE stop (
  id    TEXT PRIMARY KEY,
  name  TEXT NOT NULL,
  zone  INTEGER NOT NULL
);

CREATE TABLE link (
  from_stop TEXT NOT NULL REFERENCES stop(id),
  to_stop   TEXT NOT NULL REFERENCES stop(id),
  minutes   INTEGER NOT NULL CHECK (minutes > 0),
  PRIMARY KEY (from_stop, to_stop)
);

CREATE INDEX link_by_target ON link(to_stop);
