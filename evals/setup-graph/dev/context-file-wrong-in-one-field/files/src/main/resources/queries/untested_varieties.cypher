MATCH (v:Variety)
WHERE NOT EXISTS { (v)<-[:OF_VARIETY]-(:Lot)<-[:SOWED]-(:Trial) }
RETURN v.name AS variety
ORDER BY variety;
