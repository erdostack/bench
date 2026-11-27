CREATE TABLE players (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE matches (
    id         INTEGER PRIMARY KEY,
    played_on  TEXT NOT NULL,
    p1         INTEGER NOT NULL REFERENCES players(id),
    p2         INTEGER NOT NULL REFERENCES players(id),
    winner     INTEGER REFERENCES players(id),
    status     TEXT NOT NULL            -- 'played' or 'walkover'
);
CREATE INDEX matches_day ON matches (played_on, id);
-- edge: winner -> loser, one per played match
CREATE TABLE meetings (
    match_id   INTEGER NOT NULL,
    winner_id  INTEGER NOT NULL,
    loser_id   INTEGER NOT NULL,
    played_on  TEXT NOT NULL
);
CREATE INDEX meetings_winner ON meetings (winner_id);
CREATE INDEX meetings_loser ON meetings (loser_id);
