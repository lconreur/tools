select distinct g.id, g.organism , g.description , o.Taxo_Clade , o.Genre_espece , br.id AS 'bgc_record.id', br.category , br.product, cc.bin_label , c.gene_kind , h.id as 'hsp.id', h.cds_id , h.accession , h.env_start , h.env_stop , h.bit_score, c.orf_num , brf.family_id 
from gbk g 
inner join Organisms o on g.organism = o.alias 
inner join cds c on g.id = c.gbk_id 
inner join bgc_record br on g.id = br.gbk_id 
inner join connected_component cc on br.id = cc.record_id 
inner join hsp h on c.id = h.cds_id 
inner join bgc_record_family brf on br.id = brf.record_id 
order by g.organism , g.description , o.Taxo_Clade , o.Genre_espece , br.id, br.category , br.product
