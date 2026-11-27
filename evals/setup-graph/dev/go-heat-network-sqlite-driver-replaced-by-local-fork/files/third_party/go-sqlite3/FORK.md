# Local copy of go-sqlite3

Taken from the upstream tag v1.14.22. The one change is the bundled SQLite: sqlite3-binding.c and
sqlite3-binding.h were replaced in February 2025 with a newer amalgamation from sqlite.org, because the
planner in the bundled release chose a slow plan for our downstream walk. The version macros at the top of
sqlite3-binding.h say which release it is.

The Go sources are upstream's and are not changed. To refresh, copy the two amalgamation files over the
old ones and run `make test`. sqlite3-binding.c is stored with Git LFS.
