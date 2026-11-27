CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,            -- report | member | area
    code TEXT NOT NULL UNIQUE,
    name TEXT,                     -- areas: postcode district; reports: the district filed under
    reported_on TEXT,              -- reports: YYYY-MM-DD
    status TEXT,                   -- reports: collected | unfounded | open
    collector_code TEXT            -- reports: member code of whoever went out
);
CREATE TABLE edges (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,            -- in_area | covers | collected_by
    src INTEGER NOT NULL,
    dst INTEGER NOT NULL
);
CREATE INDEX nodes_code ON nodes (kind, code);
CREATE INDEX edges_src ON edges (src, kind);
CREATE INDEX edges_dst ON edges (dst, kind);
