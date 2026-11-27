LOAD CSV WITH HEADERS FROM 'file:///municipalities.csv' AS row
MERGE (m:Municipality {code: row.code})
  SET m.name = row.name, m.province = row.province;
