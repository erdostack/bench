-- Indexes nothing reads any more (see queries/): the search box moved to the search service, and no query
-- filters or sorts on added_at or created_at.
DROP INDEX IF EXISTS deps_added_at;
DROP INDEX IF EXISTS packages_created_at;
DROP INDEX IF EXISTS packages_lower_name;
-- deps_dep_kind stays: queries/weekly_dependents_report.sql looks packages up by dep_id every Monday (500
-- lookups); the report only shows "never used" because the statement log covers the last 24 hours.
