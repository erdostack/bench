# why: FLEET-301 two new street bays on Kiln Lane. Run on published 2026-10-14 (reviewed: p.huang).
G.add_node("B-0391", zone="Z-KILN", spaces=2, kind="street")
G.add_node("B-0392", zone="Z-KILN", spaces=2, kind="street")
G.add_edge("B-0391", "B-0392", minutes=1)
G.add_edge("B-0391", "B-0214", minutes=6)
