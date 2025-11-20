-- to find newick correspondance, record_id (le chiffre qu'on a en fin d'arbre) vs path (donnant le nom de l'organisme/scaffold/region)
select record_id, g."path"
from bgc_record_family brf  
inner join bgc_record br on brf.record_id = br.id 
inner join gbk g on br.gbk_id = g.id
--where brf.record_id = 3980