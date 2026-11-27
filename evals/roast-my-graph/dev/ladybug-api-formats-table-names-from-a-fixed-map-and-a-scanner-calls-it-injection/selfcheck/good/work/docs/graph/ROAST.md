# Roast: fieldbook api

Read with the scanner's finding in mind: where could a request value end up in query text?

## Findings

### 1. list_nodes (low)

**Problem.** Flagged by the scanner. The f-string only inserts names from TABLES; kind is a dictionary key and an unknown one raises NotFound. skip and limit are integers, clamped, and passed as $skip and $limit. Not an injection.

**Fix.** No change to the query. Add a test that /api/anything-else returns 404 and that a key value full of quotes and braces is returned as not found, so the pen testers have something to read.

### 2. TABLES (low)

**Problem.** The safety of the whole browse layer rests on these maps staying constants. A future change that builds them from configuration or the request would open it up.

**Fix.** Make them immutable (MappingProxyType or tuples) and say in the module docstring, as it already does, that they must never come from input.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
