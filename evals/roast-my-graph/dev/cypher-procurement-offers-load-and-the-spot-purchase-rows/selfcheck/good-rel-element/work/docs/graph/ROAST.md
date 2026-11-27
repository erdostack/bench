# Review

The job fails because an optional field is part of the MERGE key. Severity medium; fix described in findings.json.

## SUPPLIES.contract_ref (medium)

Problem: Used as a MERGE key although it is optional; a null merge key raises an error, failing the transaction for the entire file.

Fix: Load spot purchases with a second statement that merges SUPPLIES without contract_ref, or move contract_ref out of the MERGE into SET.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
