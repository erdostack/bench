Added flatten(conn) to shop/redirects.py. A URL in a redirect loop keeps its own to_path; I confirmed this matches
what the CMS expects.
