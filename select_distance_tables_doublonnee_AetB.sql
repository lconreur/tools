--essai seul sans union mais tables doublonnées
SELECT 
  substr(gbka.path, length(gbka.path) - instr(reverse(gbka.path), '/') + 2) AS filenameA, 
  substr(gbkb.path, length(gbkb.path) - instr(reverse(gbkb.path), '/') + 2) AS filenameB,
  d.edge_param_id,
  brfa.family_id,
  oa.Genre_espece AS Genre_espece_A,
  oa.Genus AS Genus_A,
  oa.alias AS alias_A,
  ob.Genre_espece AS Genre_espece_B,
  ob.Genus AS Genus_B,
  ob.alias AS alias_B,
  ta.Taxo_Fam AS Fam_A, ta.Taxo_Order AS Ord_A, ta.Taxo_Class AS Cla_A, ta.Taxo_Phylum AS Phy_A,
  tb.Taxo_Fam AS Fam_B, tb.Taxo_Order AS Ord_B, tb.Taxo_Class AS Cla_B, tb.Taxo_Phylum AS Phy_B,
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
INNER JOIN Organisms oa ON gbka.organism = oa.alias
INNER JOIN Organisms ob ON gbkb.organism = ob.alias
INNER JOIN Taxonomy ta ON oa.taxo_id = ta.id 
INNER JOIN Taxonomy tb ON ob.taxo_id  = tb.id 
WHERE d.distance < 0.3 AND d.distance != 0