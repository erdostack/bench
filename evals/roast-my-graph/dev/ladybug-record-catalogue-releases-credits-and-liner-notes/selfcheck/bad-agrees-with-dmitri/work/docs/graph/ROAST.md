# Review

Dmitri is right. Convert liner_notes into relationships and drop it before the import.

## Release.liner_notes (high)

Credits stored as text inside a STRING[]: they cannot be traversed, constrained or indexed.

Fix: Parse every line into CREDITED_ON relationships during the import and drop the property.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
