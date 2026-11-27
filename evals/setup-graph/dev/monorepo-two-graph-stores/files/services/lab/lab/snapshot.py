"""python -m lab.snapshot <export dir>: rebuild var/baskets.kz from the nightly CSV export."""
import shutil
import sys
from pathlib import Path

from . import graph

if __name__ == "__main__":
    export = Path(sys.argv[1])
    shutil.rmtree(graph.PATH, ignore_errors=True)
    Path(graph.PATH).parent.mkdir(exist_ok=True)
    conn = graph.connect(read_only=False)
    conn.execute("CREATE NODE TABLE Product(sku STRING, category STRING, PRIMARY KEY (sku))")
    conn.execute("CREATE REL TABLE BOUGHT_WITH(FROM Product TO Product, orders INT64)")
    conn.execute(f'COPY Product FROM "{export / "products.csv"}" (header=true)')
    conn.execute(f'COPY BOUGHT_WITH FROM "{export / "pairs.csv"}" (header=true)')
