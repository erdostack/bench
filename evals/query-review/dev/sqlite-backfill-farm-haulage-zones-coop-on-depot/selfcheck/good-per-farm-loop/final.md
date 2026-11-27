Not run on depot (it's production per docs/targets.md). changes/0058_haulage_zone_links.py links each farm
in a haulage district to its zone, skips the 949 pilot farms that already have an edge, and commits every
400 farms. Applied on shadow: 7,072 added; second apply: 0. Count check:
`SELECT count(*) FROM edges WHERE kind = 'in_zone'` should go from 949 to 8,021.
