-- Selecting a complete distance set of distances below cutoff
SELECT substr(gbka.path, length(gbka.path) - instr(reverse(gbka.path), '/') + 2) AS filenameA, 
  substr(gbka.path, length(gbkb.path) - instr(reverse(gbkb.path), '/') + 2) AS filenameB,
  o.Genre_espece,
  o.Genus,
  t.*,
  d.distance,
  d.jaccard, 
  d.adjacency, 
  d.dss, 
  d.edge_param_id,
  params.weights
FROM distance d
INNER JOIN bgc_record bgca ON bgca.id=d.record_a_id
INNER JOIN bgc_record bgcb ON bgcb.id=d.record_b_id
INNER JOIN gbk gbka ON gbka.id=bgca.gbk_id
INNER JOIN gbk gbkb ON gbkb.id=bgcb.gbk_id
INNER JOIN edge_params params ON d.edge_param_id==params.id
INNER JOIN Organisms o ON gbka.organism = o.alias
INNER JOIN Taxonomy t ON o.taxo_id = t.id 
WHERE d.distance<0.3 and d.distance != 0
ORDER BY d.distance
LIMIT 3000;