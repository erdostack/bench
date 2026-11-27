# 0021. Conflict-of-interest filter

Status: Accepted (2026-11-23)

Decision: recursive-sql

We stay on Postgres. The editor-in-chief's rule: a reviewer has a conflict if they co-authored any paper with any
of the submission's authors within the last 24 months. Only direct co-authors; never co-authors of co-authors;
institutions are not part of it. That makes it one fixed-depth join (no recursion needed) over 5.2M authorship
rows, run for about 1,800 submissions a month with under a second to answer. Bram's graph database proposal was
rejected: a new store for a single join.
