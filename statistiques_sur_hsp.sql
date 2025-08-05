--toutes les combinaisons organism-accession avec le nombre d'occurence d'hsp et le bit_score moyen
SELECT 
  gbk.organism,
  h.accession,
  COUNT(DISTINCT h.id) AS nb_hsp,
  AVG(h.bit_score) AS avg_bit_score
FROM scanned_cds sc
JOIN cds c ON sc.cds_id = c.id
JOIN gbk ON gbk.id = c.gbk_id
JOIN hsp h ON h.cds_id = sc.cds_id
GROUP BY gbk.organism, h.accession
ORDER BY gbk.organism, nb_hsp DESC;

SELECT bit_score FROM hsp;

-- moyenne
SELECT AVG(bit_score) AS moyenne
FROM hsp;

-- écart-type
SELECT 
  COUNT(*) AS n,
  AVG(bit_score) AS moyenne,
  SQRT(AVG((bit_score - (SELECT AVG(bit_score) FROM hsp)) * (bit_score - (SELECT AVG(bit_score) FROM hsp)))) AS ecart_type
FROM hsp;


--Calculer le percentile (ex : top 5 %) => 287.4508361816406
SELECT bit_score
FROM hsp
ORDER BY bit_score DESC
LIMIT 1 
OFFSET CAST(0.05 * (SELECT COUNT(*) FROM hsp) AS INT);



-- calcul 95e percentile => 287.37017822265625
SELECT bit_score
FROM hsp
ORDER BY bit_score
LIMIT 1
OFFSET (SELECT CAST(0.95 * COUNT(*) AS INTEGER) FROM hsp) - 1;


-- calcul 99e percentile => 467.1754150390625
SELECT bit_score
FROM hsp
ORDER BY bit_score
LIMIT 1
OFFSET (SELECT CAST(0.99 * COUNT(*) AS INTEGER) FROM hsp) - 1;

--filtré sur bit_score > 287 => 1255 lignes
SELECT 
  gbk.organism,
  h.accession,
  COUNT(DISTINCT h.id) AS nb_hsp,
  AVG(h.bit_score) AS avg_bit_score
FROM scanned_cds sc
JOIN cds c ON sc.cds_id = c.id
JOIN gbk ON gbk.id = c.gbk_id
JOIN hsp h ON h.cds_id = sc.cds_id
GROUP BY gbk.organism, h.accession
HAVING AVG(h.bit_score) >= 287
ORDER BY gbk.organism, nb_hsp DESC;

--filtré sur bit_score avec calcul percentile 0.95 imbriqué dans le HAVING
SELECT 
  gbk.organism,
  h.accession,
  COUNT(DISTINCT h.id) AS nb_hsp,
  AVG(h.bit_score) AS avg_bit_score
FROM scanned_cds sc
JOIN cds c ON sc.cds_id = c.id
JOIN gbk ON gbk.id = c.gbk_id
JOIN hsp h ON h.cds_id = sc.cds_id
GROUP BY gbk.organism, h.accession
HAVING AVG(h.bit_score) >= 
	(
	SELECT bit_score
	FROM hsp
	ORDER BY bit_score
	LIMIT 1
	OFFSET (SELECT CAST(0.95 * COUNT(*) AS INTEGER) FROM hsp) - 1
	)
ORDER BY gbk.organism, nb_hsp DESC;

--filtré sur bit_score avec calcul percentile 0.99 imbriqué dans le HAVING
SELECT 
  gbk.organism,
  h.accession,
  COUNT(DISTINCT h.id) AS nb_hsp,
  AVG(h.bit_score) AS avg_bit_score
FROM scanned_cds sc
JOIN cds c ON sc.cds_id = c.id
JOIN gbk ON gbk.id = c.gbk_id
JOIN hsp h ON h.cds_id = sc.cds_id
GROUP BY gbk.organism, h.accession
HAVING AVG(h.bit_score) >= 
	(
	SELECT bit_score
	FROM hsp
	ORDER BY bit_score
	LIMIT 1
	OFFSET (SELECT CAST(0.99 * COUNT(*) AS INTEGER) FROM hsp) - 1
	)
ORDER BY gbk.organism, nb_hsp DESC;
