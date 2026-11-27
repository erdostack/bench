# Review

liner_notes duplicates CREDITED_ON. Not urgent, but it should go.

## liner_notes (medium)

Denormalised multi-valued attribute duplicating the CREDITED_ON edge set; violates single source of truth and risks drift.

Fix: Deprecate the property and render the as-printed section from CREDITED_ON.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
