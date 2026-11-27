import json
p = "graphs/practice/social.json"
data = json.load(open(p))
names = {n["id"]: f"{n.get('firstName')} {n.get('lastName')}" for n in data["nodes"]}
pairs = {frozenset(x) for x in [("Leopold Ibbotson", "Edda Eskildsen"), ("Dmitri Dovey", "Mira Eskildsen"), ("Jonah Holloway", "Henrik Midgley"),
         ("Bertil Ibbotson", "Mira Kavanagh"), ("Mira Bramwell", "Edda Achterberg"), ("Saga Bramwell", "Kaia Ibbotson"),
         ("Iris Juhl", "Otto Lomax"), ("Greta Midgley", "Rasmus Lomax")]}
before = len(data["links"])
data["links"] = [l for l in data["links"] if not (l["kind"] == "knows" and frozenset((names[l["source"]], names[l["target"]])) in pairs)]
print(before - len(data["links"]))
json.dump(data, open(p, "w"))
