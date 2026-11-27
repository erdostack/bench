-- Editors can pin a related article (auto or their own) so it always shows first.
ALTER TABLE related ADD COLUMN pinned INTEGER NOT NULL DEFAULT 0;
