# Roast: metroline queries

Three queries wearing the same warning label. One of them is telling the transport board that every station on the line is exactly as busy as the entire network.

## Findings

### 1. line_ridership (critical)

**Problem.** The first MATCH collects every Tap between $from and $to, about 48 million for a month. The second collects the stations on the line. The two have no variable in common and there is no AT relationship between t and s, so the result is every tap combined with every station: each station is returned with count(t) equal to all taps in the network that month, the same number on every row, and the database has to produce taps times stations rows to compute it. The board report built on this cannot tell a busy station from an empty one.

**Fix.** Connect them through the relationship the model has for it: MATCH (t:Tap)-[:AT]->(s:Station)-[:ON]->(:Line {code: $line}) WHERE t.day >= $from AND t.day <= $to RETURN s.name AS station, count(t) AS taps ORDER BY taps DESC. Re-run the reports already sent.

### 2. same_line (low)

**Problem.** Two patterns with a comma, which is what the linter sees. Each one finds a single station by its unique code, so there is one row on each side and the following MATCH joins them. Nothing to fix.

**Fix.** Leave it, or silence the warning by writing the two lookups as separate MATCH clauses.

### 3. zone_pairs (low)

**Problem.** Pairs every zone with every zone deliberately, to list the fare table. Six zones, 21 rows.

**Fix.** Leave it.

### 4. card_mix (low)

**Problem.** Reads a whole day of taps to count card kinds. Nightly, through the tap_day index; fine.

**Fix.** Nothing.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
