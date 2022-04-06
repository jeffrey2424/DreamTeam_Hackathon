WITH ngram_counts AS
    (
    SELECT url, date, REGEXP_REPLACE(LOWER(CONCAT(ngram, " ", REGEXP_EXTRACT(post, r'([^\s]+)'))), r'[\.\",*:()\[\]/|\n@]', '') AS phrase
    FROM `gdelt-bq.gdeltv2.webngrams`
    WHERE (DATE(date) = "2022-04-06" AND LANG = "en")
    UNION ALL
    SELECT url, date, REGEXP_REPLACE(LOWER(ngram), r'[\.\",*:()\[\]/|\n@]', '') AS phrase
    FROM `gdelt-bq.gdeltv2.webngrams`
    WHERE (DATE(date) = "2022-04-06" AND LANG = "en")
    )
SELECT url, date, mid, name, article_title, relevant_mentions/total_words AS corpus_score, sentiment_score, sentiment_magnitude, sentiment_salience
FROM
    (
    SELECT url, date, COUNT(*) AS relevant_mentions
    FROM ngram_counts
    WHERE phrase IN (SELECT * FROM `hackathon-team-10.corpus.corpus`)
    GROUP BY url, date
    ) AS t1
-- Inner join with NGRAMS to get word count
INNER JOIN
    (
    SELECT url AS url2, date AS date2, COUNT(*) AS total_words
    FROM ngram_counts
    GROUP BY url, date
    ) AS t2
ON (t1.date = t2.date2) AND (t1.url = t2.url2)
-- Inner join with GDELT entities to get entity and sentiment
INNER JOIN
    (
    SELECT mid, name, magnitude AS sentiment_magnitude, score AS sentiment_score, avgSalience AS sentiment_salience
    FROM `gdelt-bq.gdeltv2.geg_gcnlapi`, UNNEST(entities)
    WHERE (avgSalience > 0.5 AND LANG = "en" AND DATE(date) = "2022-04-06" AND mid IN (SELECT mid FROM `hackathon-team-10.companies`))
    ) AS t3
ON (t1.date = t3.date) AND (t1.url = t3.url)
-- Inner join with GDELT articles to get title
INNER JOIN
    (
    SELECT url, date, title AS article_title
    FROM `gdelt-bq.gdeltv2.gal`
    WHERE (LANG = "en" AND DATE(date) = "2022-04-06")
    GROUP BY url, date
  ) AS t4
ON (t1.date = t4.date) AND (t1.url = t4.url)
ORDER BY corpus_score DESC
