CREATE TABLE models (
  id INTEGER PRIMARY KEY,
  code TEXT NOT NULL UNIQUE,        -- vendor part code, e.g. QX-6512
  band TEXT NOT NULL,
  status TEXT NOT NULL              -- current | retired
);
CREATE TABLE masts (
  id INTEGER PRIMARY KEY,
  site_code TEXT NOT NULL UNIQUE
);
CREATE TABLE antennas (
  id INTEGER PRIMARY KEY,
  mast_id INTEGER NOT NULL REFERENCES masts(id),
  model_id INTEGER NOT NULL REFERENCES models(id),
  sector INTEGER NOT NULL,
  azimuth INTEGER NOT NULL
);
CREATE TABLE spares (
  id INTEGER PRIMARY KEY,
  depot TEXT NOT NULL,
  model_code TEXT NOT NULL,         -- models.code; the stock system sends codes, not ids
  qty INTEGER NOT NULL
);
