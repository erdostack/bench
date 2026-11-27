// customers off if transformer $transformer_id trips
MATCH (m:Meter)
WHERE $transformer_id IN m.upstream_ids
RETURN count(m) AS meters_off, collect(m.address)[0..20] AS sample_addresses;
