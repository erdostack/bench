CREATE TABLE packages (
    id        INTEGER PRIMARY KEY,
    name      TEXT NOT NULL UNIQUE,
    latest    TEXT NOT NULL,
    published TEXT NOT NULL
);

-- package_id declares a dependency on dependency_id.
CREATE TABLE depends_on (
    package_id    INTEGER NOT NULL REFERENCES packages(id),
    dependency_id INTEGER NOT NULL REFERENCES packages(id),
    kind          TEXT NOT NULL CHECK (kind IN ('runtime', 'dev', 'peer')),
    PRIMARY KEY (package_id, dependency_id)
) WITHOUT ROWID;

CREATE INDEX depends_on_dependency ON depends_on(dependency_id);
