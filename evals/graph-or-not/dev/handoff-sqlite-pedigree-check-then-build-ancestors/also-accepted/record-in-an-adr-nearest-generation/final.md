sql/pedigree.sql is in. Per docs/adr/0003-pedigree-check.md the rule looks 4 generations back, so the
recursive query stops at generation 4; each ancestor is returned once with its nearest generation.
