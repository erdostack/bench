-- Used by the API to resolve /tag/<name> to an id.
SELECT id FROM tag WHERE name = :tag COLLATE NOCASE ORDER BY id LIMIT 1;
