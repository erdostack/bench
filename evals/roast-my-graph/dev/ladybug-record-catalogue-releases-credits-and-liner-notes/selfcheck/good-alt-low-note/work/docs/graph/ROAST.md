# Review

Not a relationship in disguise: the relationship exists (CREDITED_ON), and liner_notes is the printed
text. Keep it.

## Release.liner_notes (low)

Fine to keep: it is display-only source text, and the credits it describes exist as CREDITED_ON relationships. It does take space on 1.4 million releases.

Fix: Keep it; if size matters, move it to a separate node table read only by release_page.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
