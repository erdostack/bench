# fission

Teaching tool for SOC 214 (social networks). Students explore Zachary's karate club study: 34 members of
a university karate club whose friendships were recorded before the club split in two.

- `data/members.csv`: member id and the faction each joined after the split.
- `data/ties.csv`: one row per friendship; `contexts` is the number of settings (classes, the bar, the
  tournaments...) in which the two were seen interacting.
- `python -m fission.load` builds `var/club.db` from the CSVs (tables in `db/schema.sql`).
- `python -m fission.app` serves the pages on the course VM.
