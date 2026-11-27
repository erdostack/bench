"""Sends a page. The provider client lives in the pager node image; this module only formats."""


def page_text(alert_title, policy_name):
    return f"[{policy_name}] {alert_title}"
