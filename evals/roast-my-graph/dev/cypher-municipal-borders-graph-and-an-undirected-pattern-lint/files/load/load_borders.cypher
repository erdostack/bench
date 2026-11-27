// the survey lists each border twice (once per side); keep one relationship, lower code -> higher code
LOAD CSV WITH HEADERS FROM 'file:///borders.csv' AS row
WITH row WHERE row.code_a <> row.code_b
WITH CASE WHEN row.code_a < row.code_b THEN [row.code_a, row.code_b]
          ELSE [row.code_b, row.code_a] END AS pair,
     toFloat(row.length_km) AS km
MATCH (a:Municipality {code: pair[0]})
MATCH (b:Municipality {code: pair[1]})
MERGE (a)-[r:BORDERS]->(b)
  SET r.length_km = km;
