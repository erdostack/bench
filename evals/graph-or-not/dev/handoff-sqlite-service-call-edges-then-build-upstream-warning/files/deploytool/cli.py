"""deploytool: `python -m deploytool.cli <service> <version>`."""
import sqlite3
import sys
from datetime import date

from . import impact


def main(argv):
    service, version = argv[1], argv[2]
    conn = sqlite3.connect("var/deploy.db")
    callers = impact.direct_callers(conn, service, date.today().isoformat())
    print(f"deploying {service} {version}; tell: {', '.join(impact.owners(conn, callers)) or 'nobody'}")


if __name__ == "__main__":
    main(sys.argv)
