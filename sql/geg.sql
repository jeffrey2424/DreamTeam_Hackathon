SELECT url, mid, magnitude, score
FROM `gdelt-bq.gdeltv2.geg_gcnlapi`, UNNEST(entities)
WHERE (DATE(date) = "2022-04-06" AND LANG = "en" AND type = 'ORGANIZATION' AND avgSalience > 0.5)
LIMIT 100
