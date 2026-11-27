CREATE TABLE cards (
    id          INTEGER PRIMARY KEY,
    board_id    INTEGER NOT NULL,
    kind        TEXT NOT NULL CHECK (kind IN ('note', 'image', 'link', 'frame')),
    created_at  TEXT NOT NULL,
    trashed_at  TEXT
);
CREATE INDEX cards_board ON cards(board_id);
CREATE INDEX cards_trashed ON cards(trashed_at) WHERE trashed_at IS NOT NULL;

CREATE TABLE connectors (
    id          INTEGER PRIMARY KEY,
    from_card   INTEGER NOT NULL REFERENCES cards(id),
    to_card     INTEGER NOT NULL REFERENCES cards(id),
    label       TEXT,
    trashed_at  TEXT
);
CREATE INDEX connectors_from ON connectors(from_card);
CREATE INDEX connectors_to ON connectors(to_card);
CREATE INDEX connectors_trashed ON connectors(trashed_at) WHERE trashed_at IS NOT NULL;

CREATE TABLE frame_members (
    frame_id INTEGER NOT NULL REFERENCES cards(id),
    card_id  INTEGER NOT NULL REFERENCES cards(id),
    PRIMARY KEY (frame_id, card_id)
);
CREATE INDEX frame_members_card ON frame_members(card_id);
