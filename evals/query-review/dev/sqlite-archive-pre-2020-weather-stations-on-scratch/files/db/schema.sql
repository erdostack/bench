CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,          -- station | hub | sensor
    code TEXT NOT NULL UNIQUE,   -- AWS-0142, HUB-N, SN-50211
    status TEXT,                 -- station: active | retired | archived (docs/model.md)
    retired_on TEXT              -- station: YYYY-MM-DD, set when it stopped reporting
);
CREATE TABLE edges (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,          -- reports_to (station -> hub) | installed_at (sensor -> station)
    src INTEGER NOT NULL,
    dst INTEGER NOT NULL
);
CREATE INDEX edges_src ON edges (src, kind);
CREATE INDEX edges_dst ON edges (dst, kind);
