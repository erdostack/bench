flatten(conn) is in shop/redirects.py: one recursive query, as ADR 0003 decided.

Each walk carries the paths it has passed and stops when one comes round again; only walks that reach a path with no
redirect of its own produce an entry. So URLs in a loop, and URLs whose chain runs into one, are left out of the map,
which is what the ADR records as agreed with SEO. Plain SQL apart from instr(), which Postgres spells strpos(); the
prod path needs that one word swapped, or I can add a small dialect switch when write_map starts calling it.
