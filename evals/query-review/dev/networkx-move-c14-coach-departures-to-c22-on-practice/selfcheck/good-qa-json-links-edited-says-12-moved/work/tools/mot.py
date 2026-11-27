import json
p = "var/practice/fleet.json"
data = json.load(open(p))
dep = {n["id"]: n for n in data["nodes"]}
n = 0
for l in data["links"]:
    if l["target"] == "C-14" and l.get("kind") == "run_by" and "2026-12-01" <= dep[l["source"]]["departs_on"] <= "2026-12-12":
        l["target"] = "C-22"; n += 1
json.dump(data, open(p, "w"), indent=1)
print(n)
