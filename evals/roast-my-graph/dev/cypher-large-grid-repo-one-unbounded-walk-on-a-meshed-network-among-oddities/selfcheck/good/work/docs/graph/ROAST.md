# Roast: gridmap cypher/

Twenty-six statements, most of them boringly competent, a handful of them odd in the way inherited code is always odd, and one that asks the database to count every possible way electricity could wander through a city.

## Findings

### 1. downstream_meters (critical)

**Problem.** This one says: start at an asset and keep following cables, any number of them, until you reach transformers. There is no limit on how far it goes, and the network is a mesh, so between a substation and a transformer there is not one route but a great many, and the query has to try every one of them. Each junction multiplies the count. From anything upstream it will not answer in two seconds, and may not answer at all, on the screen operators use during a fault. It also walks across cables marked normally_open, which carry nothing, so even if it finished it would list meters that would not actually go dark.

**Fix.** Do not walk the cables freely. Two ways out: (1) keep the query but only follow cables where normally_open is false and give it a limit, for example MATCH (a:Asset {tag: $tag})-[cs:CONNECTS*1..25]->(t:Transformer) WHERE none(c IN cs WHERE c.normally_open) and then the SUPPLIES hop; with the open cables left out the network is a set of trees, so the routes no longer multiply. (2) Better for a screen with a time limit: have the nightly sync work out, for each transformer, which substation currently feeds it, store that as its own link, and answer this from the link.

### 2. zone_rollup (low)

**Problem.** Same shape as the dangerous one (follow WITHIN any number of times) but here it is fine: zones are a tree that is exactly four levels deep with 2,900 entries, the sync refuses anything else, and this runs overnight.

**Fix.** Leave it. Writing the range as *0..3 would make the intent obvious to the next reader.

### 3. Asset.legacy_ref (low)

**Problem.** Nothing helps the database find an asset by this value, so asset_by_old_ref looks at every asset. It is called a few times a week by two export scripts and the property is documented as on its way out.

**Fix.** Leave it; delete the property and the query when the exports go.

### 4. installed_ms (low)

**Problem.** Times are stored as millisecond counts, so nobody can read them without converting. Consistent everywhere and documented.

**Fix.** No change needed.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
