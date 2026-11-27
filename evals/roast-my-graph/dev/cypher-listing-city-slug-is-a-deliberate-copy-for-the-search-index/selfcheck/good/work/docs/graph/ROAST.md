# Roast: nookbook model

I arrived with a speech prepared about storing the same fact twice. Then I read why it is stored twice, and the speech went back in the drawer.

## Findings

### 1. Listing.city_slug (low)

**Problem.** The city is written down twice: once as the IN relationship and once as this property. Normally that is how two answers to one question start. Here it is pinned down: a listing never moves city, create_listing copies the slug from the City it has just matched, and nothing else writes it. And it earns its keep, since search_city reads one index range instead of walking 212,000 listings from the City node and sorting them.

**Fix.** Keep it. If you want a tripwire, a nightly count of listings whose city_slug differs from the slug of the City they are IN should always be zero.

### 2. search_city (low)

**Problem.** SKIP $offset still walks past every skipped row, so page 400 of a big city costs more than page 1.

**Fix.** Fine at 24 a page. If people really page deep, pass the last price and id seen instead of an offset.

Verdict: build on it. Nothing here needs fixing first.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
