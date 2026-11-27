-- Stations with no track node reachable from the core network while :section_id is closed.
WITH RECURSIVE reach(node_id) AS (
    SELECT node_id FROM track_node WHERE is_core = 1
    UNION
    SELECT CASE WHEN s.a_node = r.node_id THEN s.b_node ELSE s.a_node END
    FROM reach r
    JOIN section s ON s.a_node = r.node_id OR s.b_node = r.node_id
    WHERE s.section_id <> :section_id
)
SELECT st.station_id, st.crs, st.name
FROM station st
WHERE NOT EXISTS (SELECT 1 FROM track_node t JOIN reach r ON r.node_id = t.node_id
                  WHERE t.station_id = st.station_id)
ORDER BY st.crs;
