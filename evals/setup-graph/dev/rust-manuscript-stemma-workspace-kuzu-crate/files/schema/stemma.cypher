CREATE NODE TABLE Witness(siglum STRING, century INT64, library STRING, PRIMARY KEY (siglum));
CREATE REL TABLE COPIED_FROM(FROM Witness TO Witness, confidence DOUBLE);
