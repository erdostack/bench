Still stands: yes

We moved for one reason (docs/adr/0014-ownership-walk.md): Postgres could not meet the 800 ms p95 budget. It was 4.6 s on
61M holdings; on 44M it is 3.1 s, still almost four times over. The other way out doesn't open either: in memory
it was about 70 GB against 32 GB hosts, and 44M holdings is still around 50 GB. The graph database does the check
in 140 ms. The licence is the price of meeting the budget.
