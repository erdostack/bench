CREATE (:Control {name: 'Valley Control'});
CREATE (:Repeater {id: 'R1', site: 'Black Crag'}), (:Repeater {id: 'R2', site: 'Pike End'}),
       (:Repeater {id: 'R3', site: 'Scar Top'}), (:Repeater {id: 'R4', site: 'Moor Mast'});
CREATE (:Base {id: 'B1', name: 'North Hut'}), (:Base {id: 'B2', name: 'Lake Post'}), (:Base {id: 'B3', name: 'Quarry Base'});
MATCH (c:Control), (r1:Repeater {id: 'R1'}), (r2:Repeater {id: 'R2'}) CREATE (r1)-[:HEARS]->(c), (r2)-[:HEARS]->(c);
MATCH (r1:Repeater {id: 'R1'}), (r3:Repeater {id: 'R3'}), (r4:Repeater {id: 'R4'}), (r2:Repeater {id: 'R2'})
CREATE (r3)-[:HEARS]->(r1), (r4)-[:HEARS]->(r2), (r4)-[:HEARS]->(r1);
MATCH (b1:Base {id: 'B1'}), (b2:Base {id: 'B2'}), (b3:Base {id: 'B3'}), (r3:Repeater {id: 'R3'}), (r4:Repeater {id: 'R4'})
CREATE (b1)-[:HEARS]->(r3), (b2)-[:HEARS]->(r4), (b3)-[:HEARS]->(r3), (b3)-[:HEARS]->(r4);
