CREATE TABLE nodes (
    id     INTEGER PRIMARY KEY,
    kind   TEXT NOT NULL,          -- pool | lesson | swimmer | instructor
    code   TEXT NOT NULL UNIQUE,
    level  INTEGER                 -- lessons: 1..7, the learn-to-swim stage it teaches
);
CREATE TABLE edges (
    id    INTEGER PRIMARY KEY,
    kind  TEXT NOT NULL,           -- held_at (lesson -> pool) | taught_by (lesson -> instructor) | enrolled_in (swimmer -> lesson)
    src   INTEGER NOT NULL,
    dst   INTEGER NOT NULL
);
