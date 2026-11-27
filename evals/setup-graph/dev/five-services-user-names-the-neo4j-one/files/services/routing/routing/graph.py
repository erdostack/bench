"""Connection to the shared Memgraph."""
import os

import mgclient


def connect():
    conn = mgclient.connect(host=os.environ.get("ROUTING_MG_HOST", "localhost"),
                            port=int(os.environ.get("ROUTING_MG_PORT", "7688")))
    conn.autocommit = True
    return conn
