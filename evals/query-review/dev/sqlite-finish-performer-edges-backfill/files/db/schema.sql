CREATE TABLE artists (
    id        INTEGER PRIMARY KEY,
    name      TEXT NOT NULL,
    name_key  TEXT NOT NULL UNIQUE          -- normalised name, used to match imports
);
CREATE TABLE recordings (
    id     INTEGER PRIMARY KEY,
    title  TEXT NOT NULL,
    isrc   TEXT UNIQUE
);
-- artist -> recording. One row per artist, recording and role: an artist who sings and produces on a
-- recording has two rows. `source` is 'curated' (editors) or 'sessions' (the session-sheet backfill).
CREATE TABLE performed_on (
    artist_id     INTEGER NOT NULL REFERENCES artists(id),
    recording_id  INTEGER NOT NULL REFERENCES recordings(id),
    role          TEXT NOT NULL,
    source        TEXT NOT NULL
);
CREATE INDEX performed_on_recording ON performed_on(recording_id);
CREATE INDEX performed_on_artist ON performed_on(artist_id);
-- Session sheets from the label archive, loaded once in October 2026.
CREATE TABLE session_credits (
    id            INTEGER PRIMARY KEY,
    recording_id  INTEGER NOT NULL,
    artist_key    TEXT NOT NULL,
    role          TEXT NOT NULL
);
