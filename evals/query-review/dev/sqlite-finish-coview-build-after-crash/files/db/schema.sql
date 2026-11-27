CREATE TABLE exhibits (id INTEGER PRIMARY KEY, title TEXT NOT NULL, gallery TEXT NOT NULL);
CREATE TABLE visits (visit_id INTEGER PRIMARY KEY, started_at TEXT NOT NULL);
CREATE TABLE views (
    visit_id INTEGER NOT NULL,
    exhibit_id INTEGER NOT NULL,
    PRIMARY KEY (visit_id, exhibit_id)
) WITHOUT ROWID;
CREATE TABLE co_view (
    a INTEGER NOT NULL,
    b INTEGER NOT NULL,              -- a < b
    weight INTEGER NOT NULL,         -- number of visits that included both
    PRIMARY KEY (a, b)
) WITHOUT ROWID;
CREATE TABLE job_progress (job TEXT PRIMARY KEY, last_visit_id INTEGER NOT NULL, updated_at TEXT);
