docs/graph/ROAST.md and findings.json are written. One finding that matters: popular_near_you walks from the shopper to their country and then to every other customer in it, up to 5.8 million people and all their purchases, on every product page view. The answer is the same for everyone in a country, so compute it once an hour per country and read it back in one hop.

The other four queries are fine; buy_again gets a low-priority note. I've kept this about the query. What the hours were worth is between you and the invoice.
