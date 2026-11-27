Decision: in-process-library

Dedupe grouping, decided 2026-11-23.

Facts the user gave: link only on shared email or phone, never address. Our loop doesn't merge groups that a later
record joins (480,581 vs networkx's 464,663 groups on last week's 640k-record export). networkx: ~2 s, 560 MB.

Options: vendor graph database (no: one nightly batch), recursive SQL (no), networkx in the job (yes).

Revisit if dedupe has to answer online.
