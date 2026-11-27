// customers off if feeder $feeder_id trips
MATCH (t:Transformer)
WHERE $feeder_id IN t.upstream_ids
WITH collect(t.id) AS transformer_ids
MATCH (m:Meter)
WHERE any(x IN m.upstream_ids WHERE x IN transformer_ids)
RETURN size(transformer_ids) AS transformers_off, count(m) AS meters_off;
