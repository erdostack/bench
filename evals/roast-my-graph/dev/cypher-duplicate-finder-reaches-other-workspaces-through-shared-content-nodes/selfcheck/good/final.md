One query breaks the isolation promise, and it should be fixed before the questionnaire goes back.

duplicates_of checks that the file you start from is in your workspace. It then follows the file's content to every other file with the same content and returns their ids, names and folders without checking where those files live. Content nodes (Blob) are shared across all customers by design (docs/model.md), so anyone who uploads a common template gets a list of the names and folder paths under which other firms keep it.

The fix is one line: require the other file to be in $ws too. The remaining statements are scoped correctly; two low notes are in docs/graph/ROAST.md and findings.json.
