-- Nesting level of a post, for the indented view: 0 for the first post of a thread,
-- parent's depth + 1 for a reply. The app sets it on insert; existing rows are backfilled by a job.
ALTER TABLE posts ADD COLUMN depth INTEGER;
