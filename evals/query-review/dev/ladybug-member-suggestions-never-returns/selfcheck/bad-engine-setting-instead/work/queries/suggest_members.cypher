CALL var_length_extend_max_depth=4;
// Members to suggest to $handle: everyone within two FOLLOWS hops, in either direction
// (the people they follow or are followed by, and those people's connections).
// Parameters: $handle
// Returns: handle, displayName
MATCH (me:Member {handle: $handle})-[:FOLLOWS*]-(other:Member)
WHERE other.handle <> $handle
RETURN DISTINCT other.handle AS handle, other.displayName AS displayName
ORDER BY handle
LIMIT 50;
