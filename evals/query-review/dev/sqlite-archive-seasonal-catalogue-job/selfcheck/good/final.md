Added jobs/archive_seasonal_2025.py. It collects category 7 and everything under it with its own recursive query
rather than catalog.tree.subtree_ids: that helper has LIMIT 2000 for the menu, and this tree has 4,558 categories,
so reusing it would have left more than half of them (and their products) live. Products are archived at most 1,000
per transaction, categories 200 per transaction. On a copy it returned {'categories': 4558, 'products': 27063}.
