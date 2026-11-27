-- why: the statement as sent by the portal team, for the record
UPDATE edges SET src = (SELECT min(k.id) FROM nodes k WHERE k.kind = 'singer' AND k.ref = (SELECT d.ref FROM nodes d WHERE d.id = edges.src))
WHERE src IN (SELECT d.id FROM nodes d WHERE d.kind = 'singer' AND d.id > (SELECT min(k.id) FROM nodes k WHERE k.kind = 'singer' AND k.ref = d.ref));
DELETE FROM nodes WHERE kind = 'singer' AND id > (SELECT min(k.id) FROM nodes k WHERE k.kind = 'singer' AND k.ref = nodes.ref);
