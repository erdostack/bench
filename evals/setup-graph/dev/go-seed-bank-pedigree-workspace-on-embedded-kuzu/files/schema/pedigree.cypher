CREATE NODE TABLE Accession(id STRING, taxon STRING, origin STRING, year INT64, PRIMARY KEY (id));
CREATE REL TABLE DERIVED_FROM(FROM Accession TO Accession, method STRING, cycle INT64);
