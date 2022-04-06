SELECT * FROM
    (
    SELECT url, DATE(date) AS date, REGEXP_REPLACE(LOWER(CONCAT(ngram, " ", REGEXP_EXTRACT(post, r'([^\s]+)'))), r'[\.\",*:()\[\]/|\n@]', '') AS phrase
    FROM `gdelt-bq.gdeltv2.webngrams`
    WHERE (DATE(date) = "2022-04-06" AND LANG = "en")
    UNION ALL
    SELECT url, DATE(date) AS date, REGEXP_REPLACE(LOWER(ngram), r'[\.\",*:()\[\]/|\n@]', '') AS phrase
    FROM `gdelt-bq.gdeltv2.webngrams`
    WHERE (DATE(date) = "2022-04-06" AND LANG = "en")
    )
WHERE phrase IN ("climate change", "co2", "sustainability", "carbon", "carbon neutral")
LIMIT 100
