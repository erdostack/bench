-- Relays that can reach an uplink over links seen in the last 15 minutes with SNR of at least 5 dB.
WITH RECURSIVE good AS (
    SELECT a, b FROM link WHERE snr_db >= 5 AND seen_at > now() - interval '15 minutes'
    UNION
    SELECT b, a FROM link WHERE snr_db >= 5 AND seen_at > now() - interval '15 minutes'
),
reach(id, hops) AS (
    SELECT id, 0 FROM relay WHERE role = 'uplink'
    UNION ALL
    SELECT g.b, r.hops + 1 FROM reach r JOIN good g ON g.a = r.id
) CYCLE id SET looped USING path
SELECT id, min(hops) AS hops FROM reach WHERE NOT looped GROUP BY id ORDER BY hops, id;
