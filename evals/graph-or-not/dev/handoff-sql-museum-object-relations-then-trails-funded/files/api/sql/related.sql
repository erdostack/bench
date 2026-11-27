-- "Related objects" on an object page: everything a curator linked to it. $1 = object id
SELECT o.id, o.title, r.kind
FROM relation r
JOIN object o ON o.id = CASE WHEN r.a_id = $1 THEN r.b_id ELSE r.a_id END
WHERE r.a_id = $1 OR r.b_id = $1
ORDER BY r.kind, o.title;
