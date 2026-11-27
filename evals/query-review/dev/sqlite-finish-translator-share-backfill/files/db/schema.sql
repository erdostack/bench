CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,          -- contributor | title
    name TEXT NOT NULL
);
CREATE TABLE edges (
    src INTEGER NOT NULL,        -- contributor
    dst INTEGER NOT NULL,        -- title
    kind TEXT NOT NULL,          -- earns_on
    role TEXT NOT NULL,          -- author | translator | illustrator
    share_bp INTEGER NOT NULL,   -- share of net receipts, basis points
    contract_id TEXT NOT NULL    -- the contract the share comes from
);
CREATE INDEX edges_dst ON edges (dst, kind);
CREATE TABLE contract_import (
    contract_id TEXT PRIMARY KEY,
    contributor_id INTEGER NOT NULL,
    title_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    share_bp INTEGER NOT NULL
);
