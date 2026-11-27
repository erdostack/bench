-- why: pilots never aired are clutter on the listen-again pages too
INSERT INTO edges_archive SELECT * FROM edges WHERE (src IN (SELECT id FROM nodes WHERE kind = 'episode' AND aired_on IS NULL) OR dst IN (SELECT id FROM nodes WHERE kind = 'episode' AND aired_on IS NULL)) AND id NOT IN (SELECT id FROM edges_archive);
DELETE FROM edges WHERE id IN (SELECT id FROM edges_archive);
INSERT INTO nodes_archive SELECT * FROM nodes WHERE kind = 'episode' AND aired_on IS NULL AND id NOT IN (SELECT id FROM nodes_archive);
DELETE FROM nodes WHERE id IN (SELECT id FROM nodes_archive)
