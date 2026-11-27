"""The client page: summary, direct shareholders, documents."""
from . import sqlfile


def client_page(conn, client_id: int) -> dict:
    summary = sqlfile.fetch_all(conn, "client_summary.sql", client_id=client_id)
    if not summary:
        raise LookupError(client_id)
    company_id, name, registry_no, country, manager = summary[0]
    page = {
        "company": {"id": company_id, "name": name, "registry_no": registry_no, "country": country},
        "manager": manager,
        "shareholders": sqlfile.fetch_all(conn, "direct_shareholders.sql", company_id=company_id),
    }
    # TODO: controlled companies panel (compliance)
    return page
