# Money

Prices are agreed in whole cents. The old `cpm` column stores them as dollars in a REAL, which is not
exact (0.29 is stored as 0.28999999999999998). MON-14 moves every price to `cpm_cents`, an INTEGER of
cents: the price rounded to the nearest cent. Billing switches to `cpm_cents` on 1 December; `cpm` is
dropped after that.
