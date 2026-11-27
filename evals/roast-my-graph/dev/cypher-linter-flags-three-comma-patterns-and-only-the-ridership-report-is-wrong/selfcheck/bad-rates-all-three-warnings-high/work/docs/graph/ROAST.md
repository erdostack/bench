# Roast: metroline queries

Cartesian products, three for the price of one.

## Findings

### 1. same_line (high)

**Problem.** Cartesian product between two disconnected Station patterns on the planner hot path.

**Fix.** Rewrite as a single connected pattern.

### 2. zone_pairs (high)

**Problem.** Cartesian product of Zone with Zone; quadratic growth.

**Fix.** Precompute the pairs or connect the patterns.

### 3. line_ridership (high)

**Problem.** Cartesian product between Tap and Station: the patterns share no variable, so each station is paired with every tap and all stations get the same count.

**Fix.** MATCH (t:Tap)-[:AT]->(s:Station)-[:ON]->(l:Line {code: $line}).

Roasted with erdostack: npx skills add usergraphtheory/erdostack
