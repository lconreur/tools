-- test sur les distances = 1 qui sont très nombreuses. Focus sur Abobie1 vs Lenti6

select 
oa.Genre_espece , ob.Genre_espece , 
bgca.category , bgcb.category , 
bgca.record_number , bgcb.record_number ,
bgca.product , bgcb.product , 
brfa.family_id , brfb.family_id , 
d.distance , d.jaccard , d.adjacency , d.dss , 
gbka.path, gbkb.path, 
ca.nt_start AS nt_startA, ca.nt_stop AS nt_stopA, 
cb.nt_start AS nt_startB, cb.nt_stop AS nt_stopB

from distance d
INNER JOIN bgc_record bgca ON bgca.id = d.record_a_id
INNER JOIN bgc_record bgcb ON bgcb.id = d.record_b_id
INNER JOIN gbk gbka ON gbka.id = bgca.gbk_id
INNER JOIN gbk gbkb ON gbkb.id = bgcb.gbk_id
LEFT JOIN bgc_record_family brfa ON bgca.id = brfa.record_id
LEFT JOIN bgc_record_family brfb ON bgcb.id = brfb.record_id
INNER JOIN edge_params params ON d.edge_param_id = params.id
INNER JOIN Organisms oa ON gbka.organism = oa.alias
INNER JOIN Organisms ob ON gbkb.organism = ob.alias
INNER JOIN Taxonomy ta ON oa.taxo_id = ta.id 
INNER JOIN Taxonomy tb ON ob.taxo_id  = tb.id
INNER JOIN cds ca ON gbka.id = ca.gbk_id 
INNER JOIN cds cb ON gbkb.id = cb.gbk_id 

WHERE d.distance = 1 and oa.alias LIKE "Abobie1" and ob.alias LIKE 'Lenti6'