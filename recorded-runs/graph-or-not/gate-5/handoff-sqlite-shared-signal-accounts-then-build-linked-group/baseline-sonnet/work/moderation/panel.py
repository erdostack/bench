"""Moderator panel data."""
from moderation.links import linked_accounts


def panel(conn, account_id):
    return {"account": account_id, "linked": linked_accounts(conn, account_id)}
