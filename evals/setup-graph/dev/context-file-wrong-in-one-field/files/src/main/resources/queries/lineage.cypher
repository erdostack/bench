MATCH (lot:Lot {code: 'L-2024-017'})-[:GROWN_FROM*1..12]->(ancestor:Lot)
RETURN ancestor.code AS code, ancestor.year AS year
ORDER BY year DESC;
