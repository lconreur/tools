-- select nombre de lignes de distance par tranche de cutoff

WITH tranches AS (
  SELECT
    CASE
      WHEN d.distance = 0.0 THEN -0.1  -- Marqueur spécial pour 0
      WHEN d.distance = 1.0 THEN 1.0   -- Dernière tranche
      ELSE ROUND(FLOOR(d.distance / 0.1) * 0.1, 1)
    END AS tranche_debut,

    CASE
      WHEN d.distance = 0.0 THEN 0.0
      WHEN d.distance = 1.0 THEN 1.0
      ELSE ROUND(FLOOR(d.distance / 0.1) * 0.1 + 0.1, 1)
    END AS tranche_fin,

    COUNT(*) AS nombre_de_lignes
  FROM distance d
  WHERE d.distance <= 1.0
  GROUP BY
    CASE
      WHEN d.distance = 0.0 THEN -0.1
      WHEN d.distance = 1.0 THEN 1.0
      ELSE FLOOR(d.distance / 0.1) * 0.1
    END
)
SELECT
  CASE 
    WHEN tranche_debut = -0.1 THEN '== 0.0'
    WHEN tranche_debut = 1.0 THEN '== 1.0'
    ELSE CONCAT('[', ROUND(tranche_debut,1), ' - ', ROUND(tranche_fin,1), ')')
  END AS tranche_label,
  nombre_de_lignes,
  SUM(nombre_de_lignes) OVER (ORDER BY tranche_debut) AS cumul
FROM tranches
ORDER BY tranche_debut;