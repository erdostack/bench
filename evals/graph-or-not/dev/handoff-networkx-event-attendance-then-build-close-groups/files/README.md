# seminar-tools

Small tools for the social networks seminar. Students reproduce classic analyses on public datasets; this repo
holds the loaders and the class dashboard (a Streamlit page the TA runs during sessions).

- Python 3.12, `requirements.txt`.
- Current dataset: the Davis, Gardner and Gardner (1941) "Southern Women" attendance data, as bundled with
  networkx (`davis_southern_women_graph`): 18 women, 14 social events, who attended which.
- `python scripts/load.py` writes `var/seminar.db` (SQLite, not committed) from `data/attendance.csv`.
  Tables in `db/schema.sql`.
