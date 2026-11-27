-- why: listen-again pages time out on the back catalogue. 2026 committee cut-off, episodes aired before 2024-01-01 go to the archive (docs/archive.md)
-- Moves every edge that touches a cut-off episode at either end (docs/archive.md), not only the edges it is the src of as 0007 did. 52 repeat_of edges from newer repeats point at cut-off episodes and would otherwise be left dangling.
-- Counts: 554 episodes aired before 2024-01-01 (NULL aired_on excluded: 12 pilots stay). 9,129 edges touch them. Same rows: 554 nodes and 9,129 edges moved.
-- 30 episodes a run: at most 24 edges each, so a run changes well under the 2,000 row limit (docs/targets.md).
INSERT INTO edges_archive SELECT * FROM edges WHERE src IN (
    SELECT id FROM nodes WHERE kind = 'episode' AND aired_on < '2024-01-01' ORDER BY id LIMIT 30)
    OR dst IN (SELECT id FROM nodes WHERE kind = 'episode' AND aired_on < '2024-01-01' ORDER BY id LIMIT 30);
DELETE FROM edges WHERE src IN (
    SELECT id FROM nodes WHERE kind = 'episode' AND aired_on < '2024-01-01' ORDER BY id LIMIT 30)
    OR dst IN (SELECT id FROM nodes WHERE kind = 'episode' AND aired_on < '2024-01-01' ORDER BY id LIMIT 30);
INSERT INTO nodes_archive SELECT * FROM nodes WHERE id IN (
    SELECT id FROM nodes WHERE kind = 'episode' AND aired_on < '2024-01-01' ORDER BY id LIMIT 30);
DELETE FROM nodes WHERE id IN (
    SELECT id FROM nodes WHERE kind = 'episode' AND aired_on < '2024-01-01' ORDER BY id LIMIT 30);
