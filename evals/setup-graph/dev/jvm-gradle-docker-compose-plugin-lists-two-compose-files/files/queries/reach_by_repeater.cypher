MATCH (r:Repeater)<-[:HEARS*]-(b:Base)
RETURN r.site AS repeater, count(DISTINCT b) AS bases_relayed
ORDER BY bases_relayed DESC
