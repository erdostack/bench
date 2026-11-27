# 2. The CSV files are the source of truth

Status: accepted

The database is derived. Corrections go into `data/*.csv` through a pull request, and the loader rebuilds the
database from scratch. We do not edit the graph by hand and there is no migration tooling.

Every row in `derives.csv` needs a `kind` (borrowed, inherited, derived, calque) so that queries can tell a loan
from a regular sound-change descendant.
