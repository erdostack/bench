CREATE TABLE clubs (
    id      INTEGER PRIMARY KEY,
    name    TEXT NOT NULL,
    country TEXT NOT NULL
);
CREATE TABLE players (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
-- one row per move; ids only ever grow (the feed importer appends)
CREATE TABLE transfers (
    id        INTEGER PRIMARY KEY,
    player_id INTEGER NOT NULL REFERENCES players(id),
    from_club INTEGER NOT NULL REFERENCES clubs(id),
    to_club   INTEGER NOT NULL REFERENCES clubs(id),
    moved_on  TEXT NOT NULL,
    kind      TEXT NOT NULL CHECK (kind IN ('permanent', 'loan', 'loan_return'))
);
CREATE INDEX transfers_from ON transfers(from_club);
CREATE INDEX transfers_to ON transfers(to_club);
-- n = number of transfers from from_club to to_club, all time
CREATE TABLE club_pairs (
    from_club INTEGER NOT NULL,
    to_club   INTEGER NOT NULL,
    n         INTEGER NOT NULL,
    PRIMARY KEY (from_club, to_club)
) WITHOUT ROWID;
CREATE TABLE job_state (
    job     TEXT PRIMARY KEY,
    last_id INTEGER NOT NULL
);
