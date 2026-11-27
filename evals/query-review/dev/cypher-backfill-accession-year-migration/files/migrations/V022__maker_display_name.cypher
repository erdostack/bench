// 2,300 makers imported without a display name before the importer fix.
MATCH (m:Maker)
WHERE m.displayName IS NULL AND m.name IS NOT NULL
SET m.displayName = m.name;
