-- Package page header.
SELECT id, name, owner, created_at FROM packages WHERE name = :name;
