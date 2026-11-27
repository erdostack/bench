CREATE TABLE patch (
    id    TEXT PRIMARY KEY,
    name  TEXT NOT NULL,
    hectares REAL NOT NULL
);
CREATE TABLE corridor (
    src   TEXT NOT NULL REFERENCES patch(id),
    dst   TEXT NOT NULL REFERENCES patch(id),
    y2024 INTEGER NOT NULL DEFAULT 0,
    y2025 INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (src, dst)
);
