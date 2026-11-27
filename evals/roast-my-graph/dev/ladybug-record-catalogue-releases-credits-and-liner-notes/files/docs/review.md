## Schema review (Dmitri)

- `Release.liner_notes STRING[]` is a relationship hiding in a string list: the credits are in there as text
  ("Producer - J. Okoro"). That's the classic mistake, you can't traverse or constrain it. It should be
  edges, and the property should go before the 1.4M-release import so we don't carry it forever.
- Otherwise looks reasonable.
