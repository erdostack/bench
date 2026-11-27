// Objects whose ownership chain has a gap of more than ten years between two holders.
MATCH (o:Object)<-[a:HELD]-(:Holder), (o)<-[b:HELD]-(:Holder)
WHERE b.from_year > a.to_year + 10
  AND NOT EXISTS { MATCH (o)<-[c:HELD]-() WHERE c.from_year > a.to_year AND c.from_year < b.from_year }
RETURN o.accession AS object, a.to_year AS gap_from, b.from_year AS gap_to
ORDER BY object;
