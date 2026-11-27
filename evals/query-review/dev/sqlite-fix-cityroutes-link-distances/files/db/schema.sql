CREATE TABLE banks (
  bank_id TEXT PRIMARY KEY,
  site    TEXT NOT NULL,
  lat     REAL NOT NULL,
  lon     REAL NOT NULL
);

CREATE TABLE route_links (
  from_bank   TEXT NOT NULL REFERENCES banks(bank_id),
  to_bank     TEXT NOT NULL REFERENCES banks(bank_id),
  metres      REAL NOT NULL,
  source      TEXT NOT NULL,      -- 'cityroutes-v2' (city road data), 'site-survey' (inside a site), 'manual'
  imported_at TEXT NOT NULL,      -- UTC, ISO 8601; a re-import of the same pair overwrites the row
  PRIMARY KEY (from_bank, to_bank)
);
CREATE INDEX route_links_source ON route_links(source, imported_at);
