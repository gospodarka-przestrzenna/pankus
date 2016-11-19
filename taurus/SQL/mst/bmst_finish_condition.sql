WITH
  sncnt(cnt) AS (SELECT
      count(DISTINCT bmst_supernode)
    FROM
      bmst
    WHERE
      level=(SELECT max(level) FROM bmst)
  )
SELECT
  (SELECT
      count(DISTINCT bmst_supernode)
    FROM
      bmst
    WHERE
      level=(SELECT max(level)-1 FROM bmst) AND
      0!=(SELECT max(level) FROM bmst)
  )==(select cnt FROM sncnt) OR  (select cnt FROM sncnt)==1