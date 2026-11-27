# Regional planner

The regional planner (`planner/regional.py`) answers "how long from town A to town B" for the
operator's regional timetable app. It does not care which platform a train uses, so it runs on a
station-level graph built every night by `jobs/collapse.py` from the full network:

- nodes: the stations, with their attributes (`name`, `crs`), and no platforms;
- an edge from station A to station B when some scheduled run goes from a platform of A to a platform of
  B, with `minutes` = the fastest such run;
- nothing else: walking transfers and station-platform access links are inside a station and mean
  nothing at station level.

The full network graph is also used by the real-time layer after the job runs, so the job must not change
the graph it is given.
