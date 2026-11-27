# prereq-planner

Degree planning for a small college: which courses unlock which, and the shortest set of courses a student
still needs before a target course.

Courses and prerequisite links are two PostgreSQL tables; every traversal is a recursive CTE in `sql/`.
See `docs/adr/0003-no-graph-extension.md` for why there is no graph database here.

    docker compose up -d
    pipenv sync
    make sql FILE=sql/all_prereqs.sql
