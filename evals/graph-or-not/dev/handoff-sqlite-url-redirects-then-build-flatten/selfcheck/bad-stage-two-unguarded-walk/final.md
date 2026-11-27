Added flatten(conn) to shop/redirects.py: it loads the redirect table into a dict and follows each from_path until
it reaches a path that has no redirect of its own. Chains are short, so this is quick.
