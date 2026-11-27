# consortium-desk

Tools for the consortium secretariat: member organisations and the working groups they sit in. The CRM export
lands every night in `var/consortium.db` (schema in `db/schema.sql`); `consortium/graph.py` loads it into
networkx for the network views in the secretariat's Flask app.

    pip install -r requirements.txt
