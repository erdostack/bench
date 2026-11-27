"""Nightly planning report. Sections are functions that take a connection and return markdown."""
from netplan.db import connect


def busiest_stops(conn, n=15):
    rows = conn.execute("SELECT code, name, boardings_per_day FROM stop ORDER BY boardings_per_day DESC LIMIT ?", (n,))
    lines = ["## Busiest stops", "", "| stop | boardings/day |", "|---|---|"]
    lines += [f"| {name} ({code}) | {b:,} |" for code, name, b in rows]
    return "\n".join(lines)


def line_lengths(conn):
    rows = conn.execute("SELECT line, COUNT(*), SUM(run_minutes) FROM link GROUP BY line ORDER BY line")
    lines = ["## Lines", "", "| line | links | minutes end to end |", "|---|---|---|"]
    lines += [f"| {line} | {n} | {m:.0f} |" for line, n, m in rows]
    return "\n".join(lines)


# TODO: critical stops section (ops asked for it after the October track failure)

SECTIONS = [busiest_stops, line_lengths]


def main():
    conn = connect()
    print("\n\n".join(section(conn) for section in SECTIONS))


if __name__ == "__main__":
    main()
