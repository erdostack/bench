# fixitguides

Community DIY repair guides. LadybugDB, opened read-only by the web app; a nightly job writes.

Sizes (November 2026):
- 2.4 million `Guide` rows, 3,100 `Topic` rows, 38 `Country` rows.
- `ABOUT`: 7.9 million. Since October the editors' "tag everything" project also attaches every guide
  to the `general` topic, so `general` alone has ~2.4 million.
- `AVAILABLE_IN`: 4.1 million (`US` has 1.6 million). Countries are only shown on the guide page; nothing
  lists the guides of a country (that is done by the search service).

Page budget: the guide page (guide_page + guide_countries + related_guides) must answer in 150 ms p95.
