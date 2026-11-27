The serious one is the dates.

The export writes them day first (31/08/2026; see data/sample/leases.csv). load_leases converts the rent and the room counts to numbers but stores starts and ends exactly as they arrive, as text, and the portal sends its dates in the same format. Text is compared from the left, so expiring_leases and rent_roll_on are comparing day-of-month first: "15/02/2027" sorts before "31/08/2026". The renewal desk's list for a building is therefore not the leases that end in the next three months, and the rent roll is not the leases in force on the day.

Fix (convert on load, convert the 96,000 existing leases once, pass real dates) is in docs/graph/ROAST.md and findings.json, with two smaller notes.
