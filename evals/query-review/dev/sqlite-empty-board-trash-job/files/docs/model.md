# Model

- `cards`: everything on a board. `kind = 'frame'` cards group other cards.
- `connectors(from_card, to_card)`: arrows between two cards.
- `frame_members(frame_id, card_id)`: which cards a frame contains.

## Trash

Trashing a card sets `trashed_at` on the card and on every connector attached to it at that moment;
restoring the card clears both. A connector can also be trashed or restored on its own (select the
arrow, delete / undo), which only touches the connector. Frame membership is not trashed: a trashed
card simply stops being drawn inside its frame.
