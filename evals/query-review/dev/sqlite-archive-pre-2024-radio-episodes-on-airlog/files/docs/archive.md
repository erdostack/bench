# The archive

The listen-again pages read `nodes` and `edges`; the archive pages read `nodes_archive` and
`edges_archive`, which have the same columns.

Archiving moves old episodes out of the live tables: each episode row is copied into `nodes_archive`, and
every edge that touches it, at either end, is copied into `edges_archive`, with the same ids and values;
then those rows are deleted from `nodes` and `edges`. Shows, presenters and tracks are never archived. A
pilot that was never broadcast (`aired_on` NULL) is not archived.

The cut-off is agreed each year by the programme committee. 2026: episodes aired before 2024-01-01.
