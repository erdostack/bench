-- For the case-insensitive search box (search moved to the search service in 2026-04).
CREATE INDEX packages_lower_name ON packages(lower(name));
CREATE INDEX packages_created_at ON packages(created_at);
