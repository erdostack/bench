CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,          -- farm | plant | haulier
    key TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL
);
CREATE TABLE edges (
    id INTEGER PRIMARY KEY,
    src INTEGER NOT NULL,
    dst INTEGER NOT NULL,
    kind TEXT NOT NULL,          -- ships_to (farm -> plant, per year) | hauled_by (farm -> haulier)
    year INTEGER,                -- ships_to only
    litres INTEGER               -- ships_to only: litres shipped in that year
);
CREATE INDEX edges_src ON edges (src, kind);
CREATE INDEX edges_dst ON edges (dst, kind);
CREATE TABLE tickets (
    id INTEGER PRIMARY KEY,
    farm_id INTEGER NOT NULL,
    plant_id INTEGER NOT NULL,
    day TEXT NOT NULL,
    litres INTEGER NOT NULL
);
CREATE INDEX tickets_farm ON tickets (farm_id, day);
CREATE TABLE job_state (job TEXT PRIMARY KEY, last_farm INTEGER NOT NULL);
