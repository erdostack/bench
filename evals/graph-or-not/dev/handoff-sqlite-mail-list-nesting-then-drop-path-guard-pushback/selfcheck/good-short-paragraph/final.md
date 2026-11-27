Position: keep

The lists nest 14 levels deep, so stopping at 10 loses real recipients. And the 37 loops in the config would each be walked to the cap, since a depth column makes every lap a new row for UNION. The current query runs at 3 ms p95, well inside 500 ms, so there's nothing to gain.
