CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,          -- supplier | plant
    key TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL
);
CREATE TABLE edges (
    id INTEGER PRIMARY KEY,
    src INTEGER NOT NULL,        -- supplier
    dst INTEGER NOT NULL,        -- plant
    kind TEXT NOT NULL,          -- approved_for | supplied (one per delivery month)
    cert_no TEXT,                -- approved_for: the certificate the approval rests on
    expires_on TEXT,             -- approved_for: certificate expiry; NULL when no certificate is required
    month TEXT                   -- supplied: YYYY-MM
);
CREATE INDEX edges_src ON edges (src, kind);
CREATE TABLE holds (             -- recall investigations
    id INTEGER PRIMARY KEY,
    supplier_id INTEGER NOT NULL,
    reason TEXT NOT NULL,
    opened_on TEXT NOT NULL,
    closed_on TEXT               -- NULL while the investigation is open
);
