Nothing has to be fixed before you build on it.

The one thing that looks wrong is Listing.city_slug duplicating the IN relationship. I'd keep it: it is what lets the busiest query read straight from an index instead of sorting a whole city, and it can't go stale because listings never change city and only create_listing sets it.

Two low notes (an optional consistency check, and deep paging in search_city) are in docs/graph/ROAST.md and findings.json.
