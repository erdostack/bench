CREATE TABLE packages (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    owner       TEXT NOT NULL,
    created_at  TEXT NOT NULL
);

-- pkg_id depends on dep_id. kind: runtime, dev, optional, peer.
CREATE TABLE deps (
    pkg_id      INTEGER NOT NULL REFERENCES packages(id),
    dep_id      INTEGER NOT NULL REFERENCES packages(id),
    kind        TEXT NOT NULL,
    added_at    TEXT NOT NULL,
    PRIMARY KEY (pkg_id, dep_id)
);
