MATCH (s:Specimen)<-[:HAS_IMAGE]-(:Image)
SET s:Imaged;
