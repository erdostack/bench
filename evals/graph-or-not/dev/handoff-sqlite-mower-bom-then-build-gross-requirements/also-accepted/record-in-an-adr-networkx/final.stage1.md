Decision: in-process-library

210,000 BOM lines is small: load bom_line into a networkx DiGraph once per nightly PLM copy and walk it in
the app; 300 explosions a day is nothing. A graph database is not needed for this. Noted in
docs/adr/0006-gross-requirements.md with the scrap rule (4% per line, compounding).
