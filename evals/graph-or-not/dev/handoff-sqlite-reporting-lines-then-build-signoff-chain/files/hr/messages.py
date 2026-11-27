"""Text of the approval emails."""


def approval_request(submitter_name, approver_name, what):
    return f"Hi {approver_name}, {submitter_name} has sent you {what} to approve."
