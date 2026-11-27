-- One row per redirect created in the CMS: a request for from_path is answered with a 301 to to_path.
CREATE TABLE redirect (
    from_path   TEXT PRIMARY KEY,
    to_path     TEXT NOT NULL,
    created_at  TEXT NOT NULL,
    created_by  TEXT NOT NULL
);
CREATE INDEX redirect_to ON redirect (to_path);
