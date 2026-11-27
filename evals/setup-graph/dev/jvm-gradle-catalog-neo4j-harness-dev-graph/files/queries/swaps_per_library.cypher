MATCH (:Lot)-[s:SWAPPED_TO]->(lib:Library)
RETURN lib.name AS library, count(s) AS swaps_received
ORDER BY swaps_received DESC
