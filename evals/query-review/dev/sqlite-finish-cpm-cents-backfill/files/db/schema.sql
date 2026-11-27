CREATE TABLE campaigns (
    id          INTEGER PRIMARY KEY,
    advertiser  TEXT NOT NULL
);

CREATE TABLE episodes (
    id    INTEGER PRIMARY KEY,
    show  TEXT NOT NULL
);

CREATE TABLE ad_slots (
    id         INTEGER PRIMARY KEY,
    campaign   INTEGER NOT NULL REFERENCES campaigns(id),
    episode    INTEGER NOT NULL REFERENCES episodes(id),
    position   TEXT NOT NULL CHECK (position IN ('pre', 'mid', 'post')),
    cpm        REAL NOT NULL,      -- dollars per thousand downloads (legacy, see docs/money.md)
    cpm_cents  INTEGER             -- the same price in whole cents
);
CREATE INDEX ad_slots_episode ON ad_slots (episode);
CREATE INDEX ad_slots_campaign ON ad_slots (campaign);
