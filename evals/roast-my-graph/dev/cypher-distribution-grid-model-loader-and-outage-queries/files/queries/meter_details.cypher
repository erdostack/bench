MATCH (m:Meter {id: $meter_id})
RETURN m.id, m.address, m.upstream_ids AS transformer;
