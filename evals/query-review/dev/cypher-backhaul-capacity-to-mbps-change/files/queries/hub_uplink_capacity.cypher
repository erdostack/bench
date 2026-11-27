// Total backhaul capacity into each hub (planning dashboard).
MATCH (h:Site {kind: 'hub'})<-[l:BACKHAUL]-(:Site)
RETURN h.siteId AS hub, sum(l.capacityKbps) AS kbps
ORDER BY kbps DESC;
