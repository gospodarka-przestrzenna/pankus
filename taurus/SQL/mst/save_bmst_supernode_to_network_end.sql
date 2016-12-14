INSERT INTO network_properties
    SELECT
        start.point,
        end.point
        :supernode_level_name,
        bmst.supernode
    FROM
        bmst,
        bmst_connection,
        point as start,
        point as end
    WHERE
        bmst_connection.start=start.id AND
        bmst_connection.end=end.id AND
        bmst_connection.end=bmst.id AND
        bmst.level=:level;



