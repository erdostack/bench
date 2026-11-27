Position: keep

Yusuf, we decided to run the grouping as connected components with networkx inside the nightly job, and it was decided
on measurements:

- The in-database version (label propagation in jobs/group_crashes.sql) took 5 h 40 min for one week. The job has a
  1 hour window before the stand-up.
- The same week in networkx: 9 minutes end to end, 19 GB peak on the 64 GB batch box, which has nothing else to do at
  night. That is 4M reports and 11M links.

A recursive CTE does not change the picture: it has to carry every reachable report for every report, which is more
work than the propagation that already takes five and a half hours. On "fragile": the job reads one week of links,
computes, and writes issue ids back in one transaction; if it fails, yesterday's grouping stays. Happy to add a memory
alarm well below 64 GB.
