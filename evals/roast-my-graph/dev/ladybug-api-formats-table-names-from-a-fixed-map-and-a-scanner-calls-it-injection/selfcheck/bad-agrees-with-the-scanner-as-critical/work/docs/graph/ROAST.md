# Roast: fieldbook api

Three f-strings, three injection points.

## Findings

### 1. list_nodes (critical)

**Problem.** Cypher built with an f-string: string interpolation into a query is injection.

**Fix.** Use parameters for everything, e.g. MATCH (n:$table).

### 2. follow (critical)

**Problem.** f-string query with the relationship name interpolated.

**Fix.** Parameterise the relationship type.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
