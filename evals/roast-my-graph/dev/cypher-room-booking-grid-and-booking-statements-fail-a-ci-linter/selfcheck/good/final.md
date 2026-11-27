Neither warning is a real problem. free_grid is meant to pair every room with every slot, that is
the grid on the screen, and it is at most 920 cells; a LIMIT 100 would break it. book_cell pairs
three single-row lookups on unique keys. I found nothing that has to change before the rollout.
Details in docs/graph/ROAST.md and findings.json.
