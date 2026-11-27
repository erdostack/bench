# labmap

Research collaboration graph for the university research office. Neo4j 5.26.

    model/schema.cypher        constraints
    load/link.py               builds COAUTHORED from the publication list
    queries/report.cypher      annual report figures
    queries/profile.cypher     researcher profile page

## How collaborations are stored

One `COAUTHORED` relationship per pair of researchers who have published together, always from the
researcher with the lower id to the one with the higher id, with `papers` = number of joint papers.
The loader recomputes all pairs from the publication list every night.

## Sizes

7,400 Researcher nodes in 11 institutes, 61,000 COAUTHORED.

## Who uses what

The annual report quotes, per institute, the number of internal collaborating pairs and the average
number of joint papers per pair (`institute_collaboration`). The profile page lists a researcher's
coauthors (`coauthors`).
