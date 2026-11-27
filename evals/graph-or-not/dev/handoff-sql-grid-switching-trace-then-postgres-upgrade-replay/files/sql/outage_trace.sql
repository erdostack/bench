-- Nodes still fed from :source_node when :opened_segment is open. The client takes the difference against the
-- normal state to list customers who lose supply.
WITH RECURSIVE fed(node_id, path) AS (
    SELECT :source_node::bigint, ARRAY[:source_node::bigint]
    UNION ALL
    SELECT CASE WHEN s.a_node = f.node_id THEN s.b_node ELSE s.a_node END,
           f.path || CASE WHEN s.a_node = f.node_id THEN s.b_node ELSE s.a_node END
    FROM fed f
    JOIN segment s ON s.is_closed AND (s.a_node = f.node_id OR s.b_node = f.node_id)
    WHERE s.segment_id <> :opened_segment
      AND NOT (CASE WHEN s.a_node = f.node_id THEN s.b_node ELSE s.a_node END) = ANY (f.path)
)
SELECT DISTINCT node_id FROM fed;
