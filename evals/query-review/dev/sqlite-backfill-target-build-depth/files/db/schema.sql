CREATE TABLE targets (
    id    INTEGER PRIMARY KEY,
    label TEXT NOT NULL UNIQUE,
    kind  TEXT NOT NULL,
    depth INTEGER                    -- BLD-415: longest chain of deps below this target; 0 for no deps
);
CREATE TABLE deps (
    src INTEGER NOT NULL REFERENCES targets(id),
    dst INTEGER NOT NULL REFERENCES targets(id),
    PRIMARY KEY (src, dst)
) WITHOUT ROWID;
CREATE INDEX deps_dst ON deps(dst);
