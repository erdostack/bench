# How prices change

Prices are never edited in place. A new price is added with `set_price`, which closes the row that is
current (its `valid_to` becomes the day before the new price starts) and adds a new `PricedOn` row from
that day with `valid_to` empty. Old rows stay: finance and the schools' bursars use `price_history` to see
what a parent was charged on a given date.

Every list gets a new price on 1 August each year, and schools can ask for a change at any time (bulk
discounts, a new supplier for blazers). Most products on most lists have three to eight rows by now.

A price that starts in the future is allowed: schools often agree the August prices in June, and the new row
is added then, starting on 1 August.
