Wrote docs/graph/CONTEXT.md. Two problems: the README's SQLite 3.46 is wrong (vendor/ has 3.41.2), and the two path queries use ordered string_agg, a 3.44 feature, so they won't run on that engine.
