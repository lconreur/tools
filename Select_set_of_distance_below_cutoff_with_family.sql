--select set of distance below cutoff, with family
SELECT 
  substr(gbka.path, length(gbka.path) - instr(reverse(gbka.path), '/') + 2) AS filenameA, 
  substr(gbkb.path, length(gbkb.path) - instr(reverse(gbkb.path), '/') + 2) AS filenameB,
  d.edge_param_id,
  brfa.family_id,
  o.Genre_espece,
  o.Genus,
  o.alias,
  t.*,
  d.distance,
  d.jaccard, 
  d.adjacency, 
  d.dss, 
  params.weights,
  'A' AS amylap_role
FROM distance d
INNER JOIN bgc_record bgca ON bgca.id = d.record_a_id
INNER JOIN bgc_record bgcb ON bgcb.id = d.record_b_id
INNER JOIN gbk gbka ON gbka.id = bgca.gbk_id
INNER JOIN gbk gbkb ON gbkb.id = bgcb.gbk_id
INNER JOIN bgc_record_family brfa ON bgca.id = brfa.record_id
INNER JOIN bgc_record_family brfb ON bgcb.id = brfb.record_id
INNER JOIN edge_params params ON d.edge_param_id = params.id
INNER JOIN Organisms o ON gbka.organism = o.alias
INNER JOIN Taxonomy t ON o.taxo_id = t.id 
WHERE d.distance < 0.3 AND d.distance != 0

UNION ALL

SELECT 
  substr(gbka.path, length(gbka.path) - instr(reverse(gbka.path), '/') + 2) AS filenameA, 
  substr(gbkb.path, length(gbkb.path) - instr(reverse(gbkb.path), '/') + 2) AS filenameB,
  d.edge_param_id,
  brfb.family_id,
  o.Genre_espece,
  o.Genus,
  o.alias,
  t.*,
  d.distance,
  d.jaccard, 
  d.adjacency, 
  d.dss, 
  params.weights,
  'B' AS amylap_role
FROM distance d
INNER JOIN bgc_record bgca ON bgca.id = d.record_a_id
INNER JOIN bgc_record bgcb ON bgcb.id = d.record_b_id
INNER JOIN gbk gbka ON gbka.id = bgca.gbk_id
INNER JOIN gbk gbkb ON gbkb.id = bgcb.gbk_id
INNER JOIN bgc_record_family brfa ON bgca.id = brfa.record_id
INNER JOIN bgc_record_family brfb ON bgcb.id = brfb.record_id
INNER JOIN edge_params params ON d.edge_param_id = params.id
INNER JOIN Organisms o ON gbkb.organism = o.alias
INNER JOIN Taxonomy t ON o.taxo_id = t.id 
WHERE d.distance < 0.3 AND d.distance != 0;