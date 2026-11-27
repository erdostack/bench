Still stands: yes

The objective is 1 s p95 (docs/slo.md). SQL got worse, 5.2 s to 9.4 s, so the reason we left it is stronger.
The in-memory numbers (0.21 s to 0.38 s, 1.9 GB to 3.3 GB) remain the fallback.
