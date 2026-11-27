The stand-ins query is in sql/stand_ins.sql, in the repo at /run/work. It follows the no-graph decision on record: one step, no recursion, because swaps do not chain.

What it does:
- Takes :ingredient_id and returns (ingredient_id, name) for every ingredient that can replace it, ordered by name.
- Reads the swap table in its direction: item_a can stand in for item_b, one way only. So the rows wanted are those where item_b is the ingredient out.
- Excludes an ingredient replacing itself, in case the sheet has a row like that.

Checks I ran, on a small in-memory database built from db/schema.sql, not on the real kitchen file (var/kitchen.db is not in the repo):
- Stand-ins for Butter: Ghee, Margarine, Olive oil, in name order. A self-row for Butter was left out.
- Stand-ins for Ghee: Lard only. Lard replaces Ghee, but nothing is added for Butter, so chains are not followed.
- Ingredient with no stand-ins: empty result.
- The query plan is SEARCH on swap_b (item_b=?), so it uses the index, not a full scan.

Not done: no timing on real data, and the stand-in count per ingredient is not known beyond the average of 2.08. The decision record is unchanged; it already says no-graph.
