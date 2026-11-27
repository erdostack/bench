SELECT h.owner_id, c.name, h.pct
FROM holding h
JOIN company c ON c.id = h.owner_id
WHERE h.owned_id = :company_id
ORDER BY h.pct DESC;
