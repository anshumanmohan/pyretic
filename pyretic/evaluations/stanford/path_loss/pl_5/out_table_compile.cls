classifier size: 11
max switch rule count: 11
average switch rule count: 11
print : match: ('vlan_pcp', 0) ('vlan_id', 2)
  -> set([modify: ('vlan_pcp', 0) ('vlan_id', 12), Controller])
 match: ('vlan_pcp', 0) ('vlan_id', 3)
  -> set([Controller, modify: ('vlan_pcp', 0) ('vlan_id', 13)])
 match: ('vlan_pcp', 0) ('vlan_id', 4)
  -> set([modify: ('vlan_pcp', 0) ('vlan_id', 14), Controller])
 match: ('vlan_pcp', 0) ('vlan_id', 5)
  -> set([Controller, modify: ('vlan_pcp', 0) ('vlan_id', 13)])
 match: ('vlan_pcp', 0) ('vlan_id', 6)
  -> set([modify: ('vlan_pcp', 0) ('vlan_id', 15), Controller])
 match: ('vlan_pcp', 0) ('vlan_id', 7)
  -> set([Controller, modify: ('vlan_pcp', 0) ('vlan_id', 13)])
 match: ('vlan_pcp', 0) ('vlan_id', 8)
  -> set([Controller, modify: ('vlan_pcp', 0) ('vlan_id', 16)])
 match: ('vlan_pcp', 0) ('vlan_id', 9)
  -> set([modify: ('vlan_pcp', 0) ('vlan_id', 13), Controller])
 match: ('vlan_pcp', 0) ('vlan_id', 10)
  -> set([Controller, modify: ('vlan_pcp', 0) ('vlan_id', 17)])
 match: ('vlan_pcp', 0) ('vlan_id', 11)
  -> set([modify: ('vlan_pcp', 0) ('vlan_id', 13), Controller])
 identity
  -> set([modify: ('vlan_pcp', 0) ('vlan_id', 18)]) 
---------------------------------