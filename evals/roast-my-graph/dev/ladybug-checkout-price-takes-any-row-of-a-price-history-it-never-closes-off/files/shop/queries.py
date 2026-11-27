"""The statements of db/prices.cypher, by their `// name:` line."""
from pathlib import Path

_TEXT = (Path(__file__).resolve().parents[1] / "db" / "prices.cypher").read_text(encoding="utf-8")

Q = {}
for _block in _TEXT.split("// name: ")[1:]:
    _name, _, _body = _block.partition("\n")
    Q[_name.strip()] = _body.strip().rstrip(";")
