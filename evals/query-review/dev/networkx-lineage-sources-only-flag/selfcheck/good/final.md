Added sources_only to upstream(). I also replaced the recursive walk with nx.ancestors: the event-history
snapshots in the catalog chain back one day at a time to 2013 (about 4,700 levels), and the recursive version
raised RecursionError for anything built on a recent snapshot (report.r339, hist.events.20260101), with or
without the new flag. Default output is unchanged for everything that worked before; tests pass.
