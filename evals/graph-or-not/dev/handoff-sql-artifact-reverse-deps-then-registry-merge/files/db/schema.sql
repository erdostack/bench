-- Registry tables (MySQL 8.0), read-only for registry-impact.
CREATE TABLE artifact_version (
    id          BIGINT PRIMARY KEY,
    package     VARCHAR(200) NOT NULL,
    version     VARCHAR(64) NOT NULL,
    published_at DATETIME NOT NULL,
    UNIQUE KEY pkg_ver (package, version)
);

-- version_id depends on depends_on_id (resolved at publish time).
CREATE TABLE dependency (
    version_id     BIGINT NOT NULL,
    depends_on_id  BIGINT NOT NULL,
    PRIMARY KEY (version_id, depends_on_id),
    KEY by_target (depends_on_id)
);
