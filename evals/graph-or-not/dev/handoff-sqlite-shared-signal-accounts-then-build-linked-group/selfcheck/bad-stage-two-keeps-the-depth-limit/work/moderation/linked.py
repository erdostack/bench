from moderation.links import linked_accounts as _walk


def linked_accounts(conn, account_id):
    return _walk(conn, account_id)
