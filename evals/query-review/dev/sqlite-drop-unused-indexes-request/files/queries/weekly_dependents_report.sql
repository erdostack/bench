-- Weekly dependents report: how many packages depend on :pkg, per kind of dependency.
SELECT kind, count(*) AS dependents
FROM deps
WHERE dep_id = :pkg
GROUP BY kind
ORDER BY kind;
