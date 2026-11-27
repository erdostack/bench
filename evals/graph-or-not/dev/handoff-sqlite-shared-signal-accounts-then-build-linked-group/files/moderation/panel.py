"""Moderator panel data."""
from moderation.links import linked_accounts


def panel(conn, account_id):
    # TODO: switch to the linked-accounts lookup we decide on
    return {"account": account_id, "linked": linked_accounts(conn, account_id)}
