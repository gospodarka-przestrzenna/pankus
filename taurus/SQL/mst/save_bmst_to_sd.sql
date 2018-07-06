INSERT INTO sd_properties
    SELECT
        bmst_id,
        :supernode_level_name,
        bmst_supernode
    FROM
        bmst
    WHERE
        level=:level;
