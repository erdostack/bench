-- Relays that lose every route to an uplink if relay R-07 goes down.
WITH RECURSIVE good AS (
    SELECT a, b FROM link WHERE snr_db >= 5 AND a <> 'R-07' AND b <> 'R-07'
    UNION
    SELECT b, a FROM link WHERE snr_db >= 5 AND a <> 'R-07' AND b <> 'R-07'
),
reach(id) AS (
    SELECT id FROM relay WHERE role = 'uplink'
    UNION ALL
    SELECT g.b FROM reach r JOIN good g ON g.a = r.id
) CYCLE id SET looped USING path
SELECT r.id FROM relay r
WHERE r.id <> 'R-07' AND r.id NOT IN (SELECT id FROM reach)
ORDER BY r.id;
