CREATE TABLE parcel (
  id           BIGSERIAL PRIMARY KEY,
  tracking_no  TEXT NOT NULL UNIQUE,
  recipient    TEXT NOT NULL,
  status       TEXT NOT NULL,
  current_hub  TEXT,
  updated_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE scan_event (
  id         BIGSERIAL PRIMARY KEY,
  parcel_id  BIGINT NOT NULL REFERENCES parcel(id),
  hub        TEXT NOT NULL,
  scanned_at TIMESTAMPTZ NOT NULL
);
