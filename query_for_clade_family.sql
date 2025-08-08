SELECT g.organism , o.*, t.*, br.*, brf.*
from gbk g
inner join Organisms o on g.organism = o.alias 
LEFT join Taxonomy t on o.taxo_id = t.id
inner join bgc_record br on g.id = br.gbk_id 
left join bgc_record_family brf on br.id = brf.record_id 