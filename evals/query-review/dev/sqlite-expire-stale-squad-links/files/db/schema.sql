CREATE TABLE players (
    id        INTEGER PRIMARY KEY,
    handle    TEXT NOT NULL UNIQUE,
    platform  TEXT NOT NULL            -- 'pc', 'mobile', 'console'
);

-- One row per unordered pair (a < b) that finished at least one match together.
CREATE TABLE played_with (
    a           INTEGER NOT NULL REFERENCES players(id),
    b           INTEGER NOT NULL REFERENCES players(id),
    games       INTEGER NOT NULL,
    last_played NOT NULL,              -- end of the pair's latest match together (UTC)
    PRIMARY KEY (a, b),
    CHECK (a < b)
) WITHOUT ROWID;
CREATE INDEX played_with_b ON played_with (b, a);

CREATE TABLE banned_handles (handle TEXT PRIMARY KEY);
