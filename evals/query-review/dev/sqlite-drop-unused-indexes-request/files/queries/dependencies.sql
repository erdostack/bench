-- What :pkg depends on, by kind.
SELECT p.name, d.kind
FROM deps d
JOIN packages p ON p.id = d.dep_id
WHERE d.pkg_id = :pkg
ORDER BY d.kind, p.name;
