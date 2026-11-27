sql/conflicted_reviewers.sql is written, per ADR 0021: co-authors of the submission's authors on papers from the
past 2 years (24 months) up to :today, direct co-authors only, minus the authors themselves. The date line uses
SQLite's date(); Postgres needs `:today::date - interval '2 years'` there.
